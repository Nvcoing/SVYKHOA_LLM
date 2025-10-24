# ===== map_dataset.py =====
import torch

def map_dataset(dataset, tokenizer):
    """
    Tokenize và chuẩn hóa dataset trước khi huấn luyện.
    """
    def tokenize_batch(example):
        tok = tokenizer(
            example["text"],
            truncation=True,
            max_length=3072,
            padding="max_length"
        )
        # Gán nhãn (labels) cho mô hình language modeling
        tok["labels"] = [
            (l if l != tokenizer.pad_token_id else -100)
            for l in tok["input_ids"]
        ]
        return tok

    dataset.set_format(None)
    dataset_tokenized = dataset.map(
        tokenize_batch,
        batched=True,
        batch_size=32,
        num_proc=None,
        remove_columns=dataset.column_names,
        keep_in_memory=False,
        load_from_cache_file=True,
        desc="Tokenizing dataset..."
    )

    print("Dataset đã được tokenize, các cột hiện có:", dataset_tokenized.column_names)
    return dataset_tokenized
