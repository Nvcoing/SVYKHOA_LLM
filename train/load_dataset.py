from datasets import load_dataset, concatenate_datasets
import json, random

def build_dataset():
    # === 1. Load trực tiếp các file .parquet từ repo Hugging Face ===
    ds_diagnosis = load_dataset(
        "parquet",
        data_files="hf://datasets/NV9523/SVYKHOA/diagnosis/SVYKHOA_dataset_diagnosis.parquet",
        split="train"
    )
    ds_guide = load_dataset(
        "parquet",
        data_files="hf://datasets/NV9523/SVYKHOA/guide/SVYKHOA_dataset_guide.parquet",
        split="train"
    )
    ds_medical_talk = load_dataset(
        "parquet",
        data_files="hf://datasets/NV9523/SVYKHOA/medical_talk/SVYKHOA_dataset_medicaltalk.parquet",
        split="train"
    )
    ds_small_talk = load_dataset(
        "parquet",
        data_files="hf://datasets/NV9523/SVYKHOA/small_talk/SVYKHOA_dataset_smalltalk.parquet",
        split="train"
    )

    # === 2. Hàm format cho từng loại ===
    def format_prompt_diagnosis(example):
        data = {
            "documpent": {
                "title": example["document/title"],
                "tool": "call_tool",
                "description": example["document/description"]
            },
            "cme": {
                "title": example["cme/title"],
                "tool": "call_tool",
                "description": example["cme/description"]
            }
        }
        text = (
            f"<|begin_of_text|>\n{example['intruction']}\n"
            f"ICD10:{example['MÃ BỆNH']}-{example['TÊN BỆNH']}\n"
            f"{example['question']}\n"
            f"<label>diagnosis</label>\n"
            f"<answer>\n**{example['MÃ BỆNH']}**:{example['TÊN BỆNH']}\n"
            f"\n**Chuẩn đoán:** {example['diagnosis']}\n"
            f"**Triệu chứng:** {example['symptom']}\n</answer>\n"
            f"<tool>\n{json.dumps(data, ensure_ascii=False, indent=4)}\n</tool>\n<|end_of_text|>"
        )
        return {"text": text}

    def format_prompt_guide(example):
        data = {
            "documpent": {
                "title": example["document/title"],
                "tool": "call_tool",
                "description": example["document/description"]
            },
            "cme": {
                "title": example["cme/title"],
                "tool": "call_tool",
                "description": example["cme/description"]
            }
        }
        text = (
            f"<|begin_of_text|>\n{example['intruction']}\n"
            f"{example['question']}\n"
            f"<label>guide</label>\n"
            f"<answer>\n{example['answer']}\n</answer>\n"
            f"<tool>\n{json.dumps(data, ensure_ascii=False, indent=4)}\n</tool>\n<|end_of_text|>"
        )
        return {"text": text}

    def format_prompt_small_talk(example):
        return {
            "text": f"<|begin_of_text|>\n{example['intruction']}\n"
                    f"{example['question']}\n"
                    f"<label>small talk</label>\n"
                    f"<answer>\n{example['answer']}\n</answer>\n<|end_of_text|>"
        }

    def format_prompt_medical_talk(example):
        return {
            "text": f"<|begin_of_text|>\n{example['intruction']}\n"
                    f"{example['question']}\n"
                    f"<label>medical talk</label>\n"
                    f"<answer>\n{example['answer']}\n</answer>\n<|end_of_text|>"
        }

    # === 3. Map từng dataset để tạo text duy nhất ===
    ds_diagnosis = ds_diagnosis.map(format_prompt_diagnosis, remove_columns=ds_diagnosis.column_names)
    ds_guide = ds_guide.map(format_prompt_guide, remove_columns=ds_guide.column_names)
    ds_small_talk = ds_small_talk.map(format_prompt_small_talk, remove_columns=ds_small_talk.column_names)
    ds_medical_talk = ds_medical_talk.map(format_prompt_medical_talk, remove_columns=ds_medical_talk.column_names)

    # === 4. Gộp tất cả dataset lại và xáo trộn ===
    dataset_all = concatenate_datasets([ds_diagnosis, ds_guide, ds_small_talk, ds_medical_talk])
    dataset_all = dataset_all.shuffle(seed=42)
    
    print(f"Tổng số mẫu: {len(dataset_all)}")
    return dataset_all
