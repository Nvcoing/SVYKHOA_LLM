#!/bin/bash
# Script upload nhieu file Excel -> Parquet len HuggingFace
# chmod +x upload.sh
# ./upload.sh


PYTHON_SCRIPT="upload_data.py"
ENV_PATH="../hf-token.env"

echo "=== Upload Excel to HuggingFace Dataset Repo ==="

# Nhap Repo ID
read -p "Nhap Repo ID (mac dinh: NV9523/SVYKHOA): " REPO_ID
REPO_ID=${REPO_ID:-NV9523/SVYKHOA}

# Nhap danh sach file (cach nhau boi dau cach)
read -p "Nhap duong dan cac file Excel (.xlsx) muon upload (cach nhau boi dau cach): " FILE_LIST

# Nhap ten folder tren repo
read -p "Nhap ten folder tren repo (vd: diagnosis_data): " FOLDER_NAME

# Upload tung file
for EXCEL_FILE in $FILE_LIST; do
    if [ -f "$EXCEL_FILE" ]; then
        echo "Dang upload: $EXCEL_FILE -> folder $FOLDER_NAME tren repo $REPO_ID"
        python "$PYTHON_SCRIPT" "$REPO_ID" "$EXCEL_FILE" "$ENV_PATH" "$FOLDER_NAME"
    else
        echo "File khong ton tai: $EXCEL_FILE"
    fi
done
