import pandas as pd
from datasets import Dataset, concatenate_datasets
import json
import random
import torch
from tqdm import tqdm

def build_dataset(tokenizer):
    parquet_files = {
        "diagnosis": 'hf://datasets/NV9523/SVYKHOA/diagnosis_aug/SVYKHOA_dataset_diagnosis.parquet',
        "guide": 'hf://datasets/NV9523/SVYKHOA/guide_aug/SVYKHOA_dataset_guide.parquet',
        "medical_talk": 'hf://datasets/NV9523/SVYKHOA/medical_talk_aug/SVYKHOA_dataset_medicaltalk.parquet',
        "small_talk": 'hf://datasets/NV9523/SVYKHOA/small_talk_aug/SVYKHOA_dataset_smalltalk.parquet'
    }

    datasets_tokenized = []

    # === Các hàm format ===
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

    def tokenize_batch(example):
        tok = tokenizer(
            example["text"],
            truncation=True,
            max_length=1536,
            padding="max_length"
        )
        tok["labels"] = [
            (l if l != tokenizer.pad_token_id else -100)
            for l in tok["input_ids"]
        ]
        return tok

    # === Load và map từng file riêng biệt ===
    for name, path in parquet_files.items():
        print(f"Đang load file: {name}")
        df = pd.read_parquet(path)

        if name == "diagnosis":
            df_proc = pd.DataFrame({"text": df.apply(format_prompt_diagnosis, axis=1)})
        elif name == "guide":
            df_proc = pd.DataFrame({"text": df.apply(format_prompt_guide, axis=1)})
        elif name == "small_talk":
            df_proc = pd.DataFrame({"text": df.apply(format_prompt_small_talk, axis=1)})
        elif name == "medical_talk":
            df_proc = pd.DataFrame({"text": df.apply(format_prompt_medical_talk, axis=1)})

        ds = Dataset.from_pandas(df_proc)
        print(f"Tokenizing dataset: {name} ({len(ds)} mẫu) ...")
        ds_tok = ds.map(
            tokenize_batch,
            batched=True,
            batch_size=32,
            num_proc=1,
            remove_columns=ds.column_names
        )
        datasets_tokenized.append(ds_tok)
        print(f"Hoàn tất {name}: {len(ds_tok)} mẫu đã tokenize\n")

    # === Gộp tất cả lại và xáo trộn ===
    dataset_all = concatenate_datasets(datasets_tokenized).shuffle(seed=42)
    print(f"Đã gộp và xáo trộn toàn bộ dataset. Tổng mẫu: {len(dataset_all)}")

    return dataset_all
