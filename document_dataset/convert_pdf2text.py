import pdfplumber
import json
import logging
from pathlib import Path

# Tắt cảnh báo CropBox
logging.getLogger("pdfminer").setLevel(logging.ERROR)


def extract_pdf_text(pdf_path: str) -> str:
    """
    Trích xuất text từ file PDF và trả về chuỗi đã dump (giữ dấu \\n).
    
    :param pdf_path: Đường dẫn tới file PDF.
    :return: Chuỗi JSON-safe (\\n thay vì xuống dòng thật).
    """
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    dumped_text = json.dumps(text)
    return dumped_text


def save_text_to_file(text: str, output_path: str):
    """
    Ghi text ra file .txt
    
    :param text: Chuỗi đã được xử lý (đã dump).
    :param output_path: Đường dẫn file xuất ra.
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)
