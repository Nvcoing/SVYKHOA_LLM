import argparse
from load_model import load_model_tokenizer
from load_dataset import build_dataset
from trainer import get_trainer
from data_pre import map_dataset

def parse_args():
    parser = argparse.ArgumentParser(description="Fine-tune SVYKHOA Chatbox Model")
    parser.add_argument("--hf_token", type=str, required=True, help="Hugging Face access token")
    parser.add_argument("--repo", type=str, default="NV9523/CHAT_SVY", help="Hugging Face repo ID")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    # Load model & tokenizer
    model, tokenizer = load_model_tokenizer()

    # Load dataset
    dataset = build_dataset()
    dataset_tokenized = map_dataset(dataset, tokenizer)
    # Gọi Trainer
    trainer = get_trainer(
        model=model,
        tokenizer=tokenizer,
        dataset=dataset_tokenized,
        repo_id=args.repo,
        hf_token=args.hf_token
    )

    # Push final model
    print("Upload model cuối cùng lên Hugging Face...")
    model.push_to_hub(args.repo, token=args.hf_token)
    tokenizer.push_to_hub(args.repo, token=args.hf_token)
    print("Huấn luyện hoàn tất và đã upload model lên Hugging Face.")
# python train.py --hf_token hf_abc123 --repo NV9523/CHAT_SVY_v2 --epochs 3 --batch 4 --lr 5e-4 --save_steps 500
