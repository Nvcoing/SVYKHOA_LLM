import re

def clean_special_tags(text: str) -> str:
    text = re.sub(r'</?answer>', '', text)  # xóa <answer> và </answer>
    text = re.sub(r'</?label>', '', text)   # xóa <label> và </label>
    return text.strip()

