import pandas as pd
import google.generativeai as genai
import time
import os
from tqdm import tqdm
import json
import argparse

# ==========================
# Nhận tham số từ run.sh
# ==========================
parser = argparse.ArgumentParser()
parser.add_argument("--api_key", required=True, help="Google API Key")
parser.add_argument("--input_file", required=True, help="Đường dẫn file input JSONL")
parser.add_argument("--output_file", required=True, help="Đường dẫn file output Excel")
parser.add_argument("--prompt_file", required=True, help="Đường dẫn file prompt.txt")
args = parser.parse_args()

# ==========================
# Setup model
# ==========================
genai.configure(api_key=args.api_key)
model = genai.GenerativeModel(model_name='models/gemini-2.0-flash')

# ==========================
# Load input data
# ==========================
try:
    df_input = pd.read_json(args.input_file, lines=True)
    df_input = df_input[['text']].dropna().reset_index(drop=True)
    print(f"Đã đọc file input với {len(df_input)} dòng văn bản.")
except Exception as e:
    print(f"Lỗi khi đọc file input: {str(e)}")
    exit()

# ==========================
# Load prompt
# ==========================
with open(args.prompt_file, "r", encoding="utf-8") as f:
    prompt_template = f.read()

# ==========================
# Tạo DataFrame kết quả
# ==========================
result_columns = ["intruction", "question", "answer"]
if os.path.exists(args.output_file):
    df_result = pd.read_excel(args.output_file)
else:
    df_result = pd.DataFrame(columns=result_columns)

# ==========================
# Hàm sinh dữ liệu với retry
# ==========================
def generate_with_retry(prompt, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = model.generate_content(prompt)
            if response.text:
                return response
        except Exception as e:
            if attempt < max_retries - 1:
                wait_time = (attempt + 1) * 5
                print(f"Lỗi, thử lại sau {wait_time}s... (Lần {attempt + 1})")
                time.sleep(wait_time)
            else:
                print(f"Lỗi sau {max_retries} lần thử: {str(e)}")
                return None
    return None

# ==========================
# Hàm xử lý và lưu kết quả
# ==========================
def process_and_save(response):
    try:
        cleaned = response.text.replace('```json', '').replace('```', '').strip()
        data_list = json.loads(cleaned)

        if not isinstance(data_list, list):
            raise ValueError("Kết quả không phải là danh sách JSON.")

        global df_result
        for data in data_list:
            new_row = {
                "intruction": data.get("intruction", ""),
                "question": data.get("question", ""),
                "answer": data.get("answer", "")
            }
            df_result.loc[len(df_result)] = new_row
        return True
    except Exception as e:
        print(f"\nLỗi xử lý response: {str(e)}")
        print(f"Response gốc: {response.text[:200]}...")
        return False

# ==========================
# Main loop
# ==========================
start_row = len(df_result)
end_row = len(df_input)
processed_count = 0
start_time = time.time()

for index in tqdm(range(start_row, end_row)):
    row = df_input.iloc[index]
    retries = 0

    while retries < 3:
        try:
            dental_text = row['text'].strip()
            prompt = prompt_template.format(dental_text=dental_text)
            response = generate_with_retry(prompt)

            if response and process_and_save(response):
                processed_count += 1
                df_result.to_excel(args.output_file, index=False)
                time.sleep(2)
                break
            else:
                retries += 1
                print(f"Retry dòng {index} - Lần {retries}")
                time.sleep(3)

        except Exception as e:
            print(f"\nLỗi dòng {index}: {str(e)}")
            retries += 1
            time.sleep(3)

# ==========================
# Save final
# ==========================
df_result.to_excel(args.output_file, index=False)
total_time = (time.time() - start_time) / 60
print(f"\nHoàn thành! Đã xử lý {processed_count} dòng.")
print(f"Thời gian chạy: {total_time:.2f} phút")
print(f"File kết quả: {args.output_file}")
