import argparse
from load_model import load_model_tokenizer
from load_dataset import build_dataset
from trainer import get_trainer

def parse_args():
    parser = argparse.ArgumentParser(description="Fine-tune SVYKHOA Chatbox Model")
    parser.add_argument("--hf_token", type=str, required=True, help="Hugging Face access token")
    parser.add_argument("--repo", type=str, default="NV9523/CHAT_SVY", help="Hugging Face repo ID")
    parser.add_argument("--epochs", type=int, default=1, help="Number of training epochs")
    parser.add_argument("--batch", type=int, default=2, help="Batch size per device")
    parser.add_argument("--lr", type=float, default=1e-3, help="Learning rate")
    parser.add_argument("--save_steps", type=int, default=200, help="Steps between checkpoints")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    print("Bắt đầu fine-tune mô hình SVYKHOA Chatbox")
    print(f"Repo: {args.repo}")
    print(f"Số epoch: {args.epochs}, batch: {args.batch}, lr: {args.lr}")
    print("=" * 60)

    # Load model & tokenizer
    model, tokenizer = load_model_tokenizer()

    # Load dataset
    dataset = build_dataset()

    # Gọi Trainer
    trainer = get_trainer(
        model=model,
        tokenizer=tokenizer,
        dataset=dataset,
        repo_id=args.repo,
        hf_token=args.hf_token
    )

    # Push final model
    print("Upload model cuối cùng lên Hugging Face...")
    model.push_to_hub(args.repo, token=args.hf_token)
    tokenizer.push_to_hub(args.repo, token=args.hf_token)
    print("Huấn luyện hoàn tất và đã upload model lên Hugging Face.")
# python train.py --hf_token hf_abc123 --repo NV9523/CHAT_SVY_v2 --epochs 3 --batch 4 --lr 5e-4 --save_steps 500
