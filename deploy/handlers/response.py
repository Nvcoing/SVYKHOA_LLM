from agent_server.generate import generate_stream
from handlers.pasre_tool import extract_tool_json_from_response as parse
import json

def handle_generate_request(model, tokenizer, device, prompt: str, labels: str = ""):
    print(f"Received prompt: {prompt}")

    stream = generate_stream(model, tokenizer, device, prompt, labels)
    buffer = ""
    for chunk in stream:
        buffer += chunk
        if "<tool>" in buffer:
            if "</tool>" not in buffer:
                continue  # Chua co dong ket thuc, tiep tuc doc
            tool_json = parse(buffer)
            # Gui JSON event cho client, da duoc dump thanh string
            yield json.dumps({"event": "tool", "tool": tool_json}, ensure_ascii=False)
            return
        else:
            # Gui chunk text thong thuong
            yield chunk
