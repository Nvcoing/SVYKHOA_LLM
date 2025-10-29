def map_dataset(dataset, tokenizer):
    """
    Tokenize và chuẩn hóa dataset trước khi huấn luyện.
    """

    def tokenize_batch(example):
        tok = tokenizer(
            example["text"],
            truncation=True,
            max_length=2048,
            padding=True, 
            return_tensors=None
        )

        input_ids = tok["input_ids"]

 
        labels = [
            (token if token != tokenizer.pad_token_id else -100)
            for token in input_ids
        ]

        tok["labels"] = labels
        return tok

    dataset = dataset.map(
        tokenize_batch,
        batched=True,
        batch_size=2048,   
        remove_columns=dataset.column_names,
        desc="Tokenizing dataset..."
    )

    print("Tokenized xong | Cột:", dataset.column_names)
    return dataset
