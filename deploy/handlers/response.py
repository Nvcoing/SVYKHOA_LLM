from agent_server.generate import generate_stream
from handlers.pasre_tool import extract_tool_json_from_response as parse
from nlp.process_prompt import clean_text as clean 
from rag.augment import augment_prompt as aug
from rag.embedding_selector import EmbeddingSelector
from rag.search_engine import SearchEngine


def handle_generate_request(model, tokenizer, device, prompt: str, labels: str = "medical talk"):
    print(f"Received prompt: {prompt}")
    engine = SearchEngine()
    search_results = engine.search_all(prompt, top_k=1)
    selector = EmbeddingSelector()
    auguments_online = selector.select_relevant_content(prompt, search_results["raw_results"], top_k=1)
    auguments_local = aug(prompt, labels, n_results=1)
    prompt= clean(prompt)
    stream = generate_stream(model, tokenizer, device, prompt, labels, auguments_local, auguments_online)
    buffer = ""
    for chunk in stream:
        buffer += chunk
        if "<tool>" in buffer:
            if "</tool>" not in buffer:
                continue  # Chua co dong ket thuc, tiep tuc doc
            tool_json = parse(buffer)
            print("Extracted tool JSON:", tool_json)
            # Gui JSON event cho client, da duoc dump thanh string
            # yield json.dumps({"event": "tool", "tool": tool_json}, ensure_ascii=False)
            yield ""
            return
        else:
            # Gui chunk text thong thuong
            yield chunk
