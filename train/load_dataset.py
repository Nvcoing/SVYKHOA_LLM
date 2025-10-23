import pandas as pd
from datasets import Dataset
import json
import random

def build_dataset():
    # Đọc dữ liệu từ HuggingFace Dataset
    df_diagnosis = pd.read_parquet('hf://datasets/NV9523/SVYKHOA/diagnosis_aug/SVYKHOA_dataset_diagnosis.parquet')
    df_guide = pd.read_parquet('hf://datasets/NV9523/SVYKHOA/guide_aug/SVYKHOA_dataset_guide.parquet')
    df_medical_talk = pd.read_parquet('hf://datasets/NV9523/SVYKHOA/medical_talk_aug/SVYKHOA_dataset_medicaltalk.parquet')
    df_small_talk = pd.read_parquet('hf://datasets/NV9523/SVYKHOA/small_talk_aug/SVYKHOA_dataset_smalltalk.parquet')

    def format_prompt_diagnosis(row):
        data = {
            "documpent": {
                "title": row['document/title'],
                "tool": "call_tool",
                "description": row['document/description']
            },
            "cme": {
                "title": row['cme/title'],
                "tool": "call_tool",
                "description": row['cme/description']
            }
        }
        return (
            f"<|begin_of_text|>\n{row['intruction']}\n"
            f"ICD10:{row['MÃ BỆNH']}-{row['TÊN BỆNH']}\n"
            f"{row['question']}\n"
            f"<label>diagnosis</label>\n"
            f"<answer>\n**{row['MÃ BỆNH']}**:{row['TÊN BỆNH']}\n"
            f"\n**Chuẩn đoán:** {row['diagnosis']}\n"
            f"**Triệu chứng:** {row['symptom']}\n</answer>\n"
            f"<tool>\n{json.dumps(data, ensure_ascii=False, indent=4)}\n</tool>\n<|end_of_text|>"
        )

    def format_prompt_guide(row):
        data = {
            "documpent": {
                "title": row['document/title'],
                "tool": "call_tool",
                "description": row['document/description']
            },
            "cme": {
                "title": row['cme/title'],
                "tool": "call_tool",
                "description": row['cme/description']
            }
        }
        return (
            f"<|begin_of_text|>\n{row['intruction']}\n"
            f"{row['question']}\n"
            f"<label>guide</label>\n"
            f"<answer>\n{row['answer']}\n</answer>\n"
            f"<tool>\n{json.dumps(data, ensure_ascii=False, indent=4)}\n</tool>\n<|end_of_text|>"
        )

    def format_prompt_small_talk(row):
        return (
            f"<|begin_of_text|>\n{row['intruction']}\n"
            f"{row['question']}\n"
            f"<label>small talk</label>\n"
            f"<answer>\n{row['answer']}\n</answer>\n<|end_of_text|>"
        )

    def format_prompt_medical_talk(row):
        return (
            f"<|begin_of_text|>\n{row['intruction']}\n"
            f"{row['question']}\n"
            f"<label>medical talk</label>\n"
            f"<answer>\n{row['answer']}\n</answer>\n<|end_of_text|>"
        )

    # Gộp tất cả lại thành một DataFrame duy nhất
    df_all = pd.concat([
        pd.DataFrame({"text": df_diagnosis.apply(format_prompt_diagnosis, axis=1)}),
        pd.DataFrame({"text": df_guide.apply(format_prompt_guide, axis=1)}),
        pd.DataFrame({"text": df_small_talk.apply(format_prompt_small_talk, axis=1)}),
        pd.DataFrame({"text": df_medical_talk.apply(format_prompt_medical_talk, axis=1)}),
    ], ignore_index=True)

    # Chuyển thành Dataset và xáo trộn
    dataset = Dataset.from_pandas(df_all)
    dataset = dataset.shuffle(seed=42)  # random seed để xáo ngẫu nhiên mỗi lần

    return dataset
