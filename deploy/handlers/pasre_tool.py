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

