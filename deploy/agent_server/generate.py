import torch
import threading
from transformers import TextIteratorStreamer
def build_prompt(prompt: str, labels: str = "") -> str:
    prompts = (
            f"<|begin_of_text|>\nBạn là Vy một trợ lý ảo về Y khoa và hãy xác định mã bệnh xem nên gọi tool và trả ra json khi nào\n{prompt.strip()}\n{labels.strip()}"
    )
    return prompts
def generate_stream(model, tokenizer, device, prompt: str,labels: str = ""):
    input_ids = tokenizer(
        build_prompt(prompt, labels),
        return_tensors="pt",
        truncation=True,
        max_length=1024
    ).input_ids.to(device)

    model.eval()

    streamer = TextIteratorStreamer(
        tokenizer,
        skip_prompt=True,
        skip_special_tokens=True
    )

    generation_kwargs = dict(
        input_ids=input_ids,
        max_new_tokens=1024,
        do_sample=True,
        temperature=0.1,
        top_k=50,
        top_p=0.95,
        repetition_penalty=1.0,
        eos_token_id=tokenizer.eos_token_id,
        pad_token_id=tokenizer.pad_token_id or tokenizer.eos_token_id,
        streamer=streamer
    )

    # Run generation in a background thread
    thread = threading.Thread(target=model.generate, kwargs=generation_kwargs)
    thread.start()

    # Yield new text as it is streamed
    for new_text in streamer:
        yield new_text
