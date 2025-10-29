def map_dataset(dataset, tokenizer):
    """
    Tokenize và chuẩn hóa dataset trước khi huấn luyện.
    """

    def tokenize_batch(example):
        tok = tokenizer(
            example["text"],
            truncation=True,
            max_length=2048,  # giảm từ 3072 để giữ phần cuối (end token)
            padding=False,    # KHÔNG pad max_length để tránh -100 chiếm hết loss
            return_tensors=None
        )

        input_ids = tok["input_ids"]

        # labels = copy input_ids
        labels = input_ids.copy()

        # Mask token PAD cho LM loss
        labels = [
            (token if token != tokenizer.pad_token_id else -100)
            for token in labels
        ]

        tok["labels"] = labels
        return tok

    dataset.set_format(None)

    dataset_tokenized = dataset.map(
        tokenize_batch,
        batched=True,
        batch_size=1024,
        num_proc=None,
        remove_columns=dataset.column_names,
        keep_in_memory=False,
        load_from_cache_file=True,
        desc="Tokenizing dataset..."
    )

    print("Tokenized xong | Cột:", dataset_tokenized.column_names)
    return dataset_tokenized
