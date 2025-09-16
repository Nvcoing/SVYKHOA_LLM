#!/bin/bash
# chmod +x upload_all.sh
# ./upload_all.sh

set -e  # dung lai neu co loi

echo "=== Upload dataset diagnosis ==="
python upload_data.py NV9523/SVYKHOA ../generate_dataset/SVYKHOA_dataset_diagnosis.xlsx diagnosis

echo "=== Upload dataset guide ==="
python upload_data.py NV9523/SVYKHOA ../generate_dataset/SVYKHOA_dataset_guide.xlsx guide

echo "=== Upload dataset medical_talk ==="
python upload_data.py NV9523/SVYKHOA ../generate_dataset/SVYKHOA_dataset_medicaltalk.xlsx medical_talk

echo "=== Upload dataset small_talk ==="
python upload_data.py NV9523/SVYKHOA ../generate_dataset/SVYKHOA_dataset_smalltalk.xlsx small_talk

echo "=== Done ==="
