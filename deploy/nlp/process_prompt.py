import re

def clean_text(text: str) -> str:
    """Xử lý text rỗng, ký tự đặc biệt"""
    text = text.strip()
    if not text or re.fullmatch(r"[\W_]+", text):
        return ""
    return "Hãy trả lời như sau: Xin chào! 👋 Rất vui được trò chuyện với bạn. Mình có thể giúp gì cho bạn hôm nay? Bạn cần mình hỗ trợ gì không?"
