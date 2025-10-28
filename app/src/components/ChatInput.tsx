import { useState } from "react";
import { Button } from "./ui/button";
import { Textarea } from "./ui/textarea";
import { Send } from "lucide-react";

interface ChatInputProps {
  onSendMessage: (message: string) => void;
  disabled?: boolean;
}

export function ChatInput({ onSendMessage, disabled }: ChatInputProps) {
  const [message, setMessage] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (message.trim() && !disabled) {
      onSendMessage(message.trim());
      setMessage("");
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="relative">
      <Textarea
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder="Nhập câu hỏi của bạn..."
        className="min-h-[70px] pr-12 bg-white border-2 border-border hover:border-primary/50 focus:border-primary resize-none shadow-sm"
        disabled={disabled}
      />
      <Button 
        type="submit" 
        size="sm" 
        disabled={!message.trim() || disabled}
        className="absolute bottom-3 right-3 h-9 w-9 p-0 bg-primary hover:bg-primary/90"
      >
        <Send className="h-4 w-4" />
      </Button>
    </form>
  );
}