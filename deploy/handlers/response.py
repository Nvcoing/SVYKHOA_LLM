from agent_server.generate import generate_stream
from pasre_tool import extract_tool_json_from_response as parse

def handle_generate_request(model, tokenizer, device, prompt: str, labels: str = ""):
    print(f"Received prompt: {prompt}")

    # tao generator
    stream = generate_stream(model, tokenizer, device, prompt, labels)

    buffer = ""
    for chunk in stream:
        buffer += chunk
        # Neu gap the <tool> thi dung
        if "<tool>" in buffer:
            tool_json = parse(buffer)
            yield {"event": "tool", "tool": tool_json}
            return
        else:
            yield {"event": "text", "data": chunk}
