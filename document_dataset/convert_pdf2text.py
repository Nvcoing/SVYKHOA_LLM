# file: pdf_to_excel.py
import os
import re
import PyPDF2
import pandas as pd
import argparse

def clean_text(text):
    if not isinstance(text, str):
        return text
    # Loại bỏ các ký tự điều khiển không hợp lệ cho Excel (\x00–\x08, \x0B, \x0C, \x0E–\x1F)
    return re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F]', '', text)

def extract_text_by_page(pdf_path):
    with open(pdf_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            yield i + 1, clean_text(text.strip()) if text else ""

def convert_pdfs_to_chunks(folder_path, output_excel):
    data = []

    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(folder_path, filename)
            print(f"Đang xử lý: {filename}")

            for page_num, page_text in extract_text_by_page(pdf_path):
                data.append({
                    "File": filename,
                    "Page": page_num,
                    "Text": page_text
                })

    df = pd.DataFrame(data)
    df.to_excel(output_excel, index=False)
    print(f"Đã lưu kết quả vào: {output_excel}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert PDFs in a folder to an Excel file with text by page.")
    parser.add_argument("--folder", type=str, required=True, help="Đường dẫn thư mục chứa PDF")
    parser.add_argument("--output", type=str, required=True, help="Tên file Excel xuất ra")

    args = parser.parse_args()
    convert_pdfs_to_chunks(args.folder, args.output)
