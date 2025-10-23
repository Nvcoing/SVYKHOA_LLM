import os
import torch
from transformers import Trainer, TrainingArguments, DataCollatorForLanguageModeling, TrainerCallback
from huggingface_hub import upload_folder, snapshot_download

# ===== 1. Callback tự động push checkpoint =====
class CheckpointPush(TrainerCallback):
    def __init__(self, repo_id: str, token: str, save_steps: int):
        self.repo_id = repo_id
        self.token = token
        self.save_steps = save_steps

    def on_save(self, args, state, control, **kwargs):
        if state.is_local_process_zero:
            ckpt_path = os.path.join(args.output_dir, f"checkpoint-{state.global_step}")
            if os.path.isdir(ckpt_path):
                upload_folder(
                    folder_path=ckpt_path,
                    repo_id=self.repo_id,
                    token=self.token,
                    path_in_repo=f"checkpoint-{state.global_step}",
                    commit_message=f"Upload checkpoint-{state.global_step}"
                )
                print(f"Uploaded checkpoint-{state.global_step} lên Hugging Face")
        return control


# ===== 2. Hàm tìm checkpoint gần nhất =====
def find_last_checkpoint(local_dir: str):
    last_ckpt = None
    max_step = -1
    for root, dirs, _ in os.walk(local_dir):
        for d in dirs:
            if "checkpoint" in d:
                try:
                    step = int(d.split("-")[-1])
                    if step > max_step:
                        max_step = step
                        last_ckpt = os.path.join(root, d)
                except:
                    continue
    return last_ckpt


# ===== 3. Hàm tạo Trainer có upload + resume =====
def get_trainer(model, tokenizer, dataset, repo_id="NV9523/CHAT_SVY", hf_token=None):
    # === 3.1 Tokenize dữ liệu trước khi huấn luyện ===
    def tokenize_batch(example):
        tok = tokenizer(
            example["text"],
            truncation=True,
            max_length=1500,
            padding="max_length"
        )
        tok["labels"] = [
            (l if l != tokenizer.pad_token_id else -100)
            for l in tok["input_ids"]
        ]
        return tok
    dataset.set_format(None)
    # Xoá toàn bộ cột cũ, chỉ giữ tokenized fields
    dataset_tokenized = dataset.map(
        tokenize_batch,
        batched=True,
        batch_size=32,              
        num_proc=None,
        remove_columns=dataset.column_names,
        keep_in_memory=False,         
        load_from_cache_file=True,
    )

    print("Dataset sau khi tokenize:", dataset_tokenized.column_names)

    # === 3.2 Cấu hình huấn luyện ===
    data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)

    training_args = TrainingArguments(
        output_dir="SVYKHOA_Chatbox",
        per_device_train_batch_size=1,
        gradient_accumulation_steps=1,
        num_train_epochs=1,
        learning_rate=1e-3,
        fp16=True,
        logging_steps=100,
        save_strategy="steps",
        save_steps=500,  # Lưu checkpoint mỗi 500 bước
        save_total_limit=1,
        remove_unused_columns=False,  #  Cần thiết cho causal LM
        report_to=["none"]
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=dataset_tokenized,
        data_collator=data_collator,
        tokenizer=tokenizer,
        callbacks=[CheckpointPush(repo_id, hf_token, training_args.save_steps)]
    )

    # === 3.3 Resume checkpoint từ repo HF nếu có ===
    print("Đang kiểm tra checkpoint từ repo HF...")
    local_ckpt_dir = snapshot_download(repo_id=repo_id, token=hf_token)
    last_ckpt = find_last_checkpoint(local_ckpt_dir)
    if last_ckpt:
        print(f"Tiếp tục huấn luyện từ checkpoint: {last_ckpt}")

        # Patch tránh lỗi weights_only
        original_load_rng_state = trainer._load_rng_state
        def patched_load_rng_state(checkpoint):
            rng_file = os.path.join(checkpoint, "rng_state.pth")
            if os.path.isfile(rng_file):
                return torch.load(rng_file, weights_only=False)
            return None
        trainer._load_rng_state = patched_load_rng_state

        trainer.train(resume_from_checkpoint=last_ckpt)
    else:
        print("Bắt đầu huấn luyện mới hoàn toàn.")
        trainer.train()

    return trainer
