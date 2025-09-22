from agent_server.generate import generate_stream

def handle_generate_request(model, tokenizer, device, prompt: str, labels: str = ""):
    print(f"Received prompt: {prompt}")
    return generate_stream(model, tokenizer, device, prompt, labels)