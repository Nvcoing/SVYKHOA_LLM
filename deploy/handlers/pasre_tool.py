import re
import json

def extract_tool_json_from_response(response_text):
    match = re.search(r"<tool>\s*(\{.*\})\s*</tool>", response_text, re.DOTALL)
    if match:
        json_str = match.group(1)
        try:
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            print("JSON decode error:", e)
            return None
    return None

# Vi du: chatbot tra ve text
response = """
<|begin_of_text|>
Hướng dẫn: ...
Câu hỏi: ...
<label>guide</label>
<answer>
Câu trả lời của chatbot
</answer>
<tool>
{
    "documpent": {
        "title": "Tên tài liệu",
        "tool": "call_tool",
        "description": "Mô tả tài liệu"
    },
    "cme": {
        "title": "Tên CME",
        "tool": "call_tool",
        "description": "Mô tả CME"
    }
}
</tool>
<|end_of_text|>
"""

tool_data = extract_tool_json_from_response(response)
print(tool_data)
