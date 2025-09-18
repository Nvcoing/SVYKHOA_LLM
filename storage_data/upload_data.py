import os
import sys
import pandas as pd
from huggingface_hub import upload_file
from dotenv import load_dotenv  # pip install python-dotenv


def load_hf_token() -> str:
    """Lay token HuggingFace tu bien moi truong hoac file .env"""
    # Load file .env neu co
    load_dotenv()

    token = os.getenv("HF_TOKEN")
    if not token:
        raise ValueError("Khong tim thay HF_TOKEN trong bien moi truong hoac file .env")
    return token


def upload_excel_to_parquet(repo_id: str, excel_file: str, folder_name: str, hf_token: str):
    """Chuyen Excel -> Parquet va upload len HuggingFace Repo"""

    # Doc file Excel/CSV
    if excel_file.endswith((".xlsx", ".xls")):
        df = pd.read_excel(excel_file)
    else:
        df = pd.read_csv(excel_file)

    # Chuyen sang parquet
    parquet_path = excel_file.rsplit(".", 1)[0] + ".parquet"
    df.to_parquet(parquet_path, index=False)

    # Tao path remote: <folder_name>/<file.parquet>
    remote_path = f"{folder_name}/{os.path.basename(parquet_path)}"

    # Upload len HuggingFace repo
    upload_file(
        path_or_fileobj=parquet_path,
        path_in_repo=remote_path,
        repo_id=repo_id,
        repo_type="dataset",
        token=hf_token,
    )

    print(f"Uploaded {parquet_path} -> {remote_path} in {repo_id}")


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Cach dung: python upload_data.py <repo_id> <file_path> <folder_name>")
        sys.exit(1)

    repo_id = sys.argv[1]
    file_path = sys.argv[2]
    folder_name = sys.argv[3]

    # Load token an toan
    hf_token = load_hf_token()

    # Upload file
    upload_excel_to_parquet(repo_id, file_path, folder_name, hf_token)
# python upload_data.py NV9523/SVYKHOA ../generate_dataset/SVYKHOA_dataset_smalltalk smalltalk
