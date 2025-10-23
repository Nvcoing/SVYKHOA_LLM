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

    # ==== Các hàm format text ====
    def format_prompt_diagnosis(row):
        data = {
            "documpent": {
                "title": row.get('document/title', ''),
                "tool": "call_tool",
                "description": row.get('document/description', '')
            },
            "cme": {
                "title": row.get('cme/title', ''),
                "tool": "call_tool",
                "description": row.get('cme/description', '')
            }
        }
        return (
            f"<|begin_of_text|>\n{row.get('intruction', '')}\n"
            f"ICD10:{row.get('MÃ BỆNH', '')}-{row.get('TÊN BỆNH', '')}\n"
            f"{row.get('question', '')}\n"
            f"<label>diagnosis</label>\n"
            f"<answer>\n**{row.get('MÃ BỆNH', '')}**:{row.get('TÊN BỆNH', '')}\n"
            f"\n**Chuẩn đoán:** {row.get('diagnosis', '')}\n"
            f"**Triệu chứng:** {row.get('symptom', '')}\n</answer>\n"
            f"<tool>\n{json.dumps(data, ensure_ascii=False, indent=4)}\n</tool>\n<|end_of_text|>"
        )

    def format_prompt_guide(row):
        data = {
            "documpent": {
                "title": row.get('document/title', ''),
                "tool": "call_tool",
                "description": row.get('document/description', '')
            },
            "cme": {
                "title": row.get('cme/title', ''),
                "tool": "call_tool",
                "description": row.get('cme/description', '')
            }
        }
        return (
            f"<|begin_of_text|>\n{row.get('intruction', '')}\n"
            f"{row.get('question', '')}\n"
            f"<label>guide</label>\n"
            f"<answer>\n{row.get('answer', '')}\n</answer>\n"
            f"<tool>\n{json.dumps(data, ensure_ascii=False, indent=4)}\n</tool>\n<|end_of_text|>"
        )

    def format_prompt_small_talk(row):
        return (
            f"<|begin_of_text|>\n{row.get('intruction', '')}\n"
            f"{row.get('question', '')}\n"
            f"<label>small talk</label>\n"
            f"<answer>\n{row.get('answer', '')}\n</answer>\n<|end_of_text|>"
        )

    def format_prompt_medical_talk(row):
        return (
            f"<|begin_of_text|>\n{row.get('intruction', '')}\n"
            f"{row.get('question', '')}\n"
            f"<label>medical talk</label>\n"
            f"<answer>\n{row.get('answer', '')}\n</answer>\n<|end_of_text|>"
        )

    # ==== Hàm tokenize batched an toàn ====
    def tokenize_batch(batch):
        texts = [t if isinstance(t, str) else "" for t in batch["text"]]
        tok = tokenizer(
            texts,
            truncation=True,
            max_length=2048,
            padding="max_length"
        )
        tok["labels"] = [
            [(l if l != tokenizer.pad_token_id else -100) for l in ids]
            for ids in tok["input_ids"]
        ]
        return tok

    # ==== Load và xử lý từng file ====
    for name, path in parquet_files.items():
        print(f"\nĐang load file: {name}")
        df = pd.read_parquet(path)

        if name == "diagnosis":
            df_proc = pd.DataFrame({"text": df.apply(format_prompt_diagnosis, axis=1)})
        elif name == "guide":
            df_proc = pd.DataFrame({"text": df.apply(format_prompt_guide, axis=1)})
        elif name == "small_talk":
            df_proc = pd.DataFrame({"text": df.apply(format_prompt_small_talk, axis=1)})
        elif name == "medical_talk":
            df_proc = pd.DataFrame({"text": df.apply(format_prompt_medical_talk, axis=1)})

        df_proc = df_proc.dropna(subset=["text"])
        df_proc = df_proc[df_proc["text"].apply(lambda x: isinstance(x, str) and x.strip() != "")]
        print(f"Sau khi làm sạch: {len(df_proc)} mẫu còn lại")

        ds = Dataset.from_pandas(df_proc)
        print(f"Tokenizing dataset: {name} ({len(ds)} mẫu) ...")

        ds_tok = ds.map(
            tokenize_batch,
            batched=True,                  # ✅ xử lý batch đúng cách
            batch_size=32,
            num_proc=1,
            remove_columns=ds.column_names,
            load_from_cache_file=False
        )

        datasets_tokenized.append(ds_tok)
        print(f"Hoàn tất {name}: {len(ds_tok)} mẫu đã tokenize\n")

    # ==== Gộp và xáo trộn ====
    dataset_all = concatenate_datasets(datasets_tokenized).shuffle(seed=random.randint(0, 9999))
    print(f"Đã gộp và xáo trộn toàn bộ dataset. Tổng mẫu: {len(dataset_all)}")

    return dataset_all
