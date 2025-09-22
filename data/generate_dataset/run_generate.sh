#!/bin/bash
# ==========================
# Biến cấu hình
# ==========================
API_KEY="YOUR_API_KEY_HERE"
INPUT_FILE="hf://datasets/hieule/youtobe_comment_vie/youtobe_comment_vie.jsonl"
OUTPUT_FILE="SVYKHOA_dataset_smalltalk.xlsx"
PROMPT_FILE="prompt.txt"

# ==========================
# Chạy Python script
# ==========================
echo "=== Bắt đầu chạy gen_dataset ==="
python gen_dataset.py \
    --api_key "$API_KEY" \
    --input_file "$INPUT_FILE" \
    --output_file "$OUTPUT_FILE" \
    --prompt_file "$PROMPT_FILE"
echo "=== Hoàn thành! ==="
