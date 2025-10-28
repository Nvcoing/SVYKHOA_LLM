import { Avatar, AvatarFallback } from "./ui/avatar";
import { Stethoscope } from "lucide-react";

export function TypingIndicator() {
  return (
    <div className="px-6 py-6 border-b border-border bg-accent/30">
      <div className="flex gap-4 max-w-none">
        <Avatar className="h-9 w-9 flex-shrink-0 border-2 border-border">
          <AvatarFallback className="bg-emerald-500 text-white">
            <Stethoscope className="h-4 w-4" />
          </AvatarFallback>
        </Avatar>
        
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 mb-3">
            <span className="font-medium text-foreground">Trợ lý Y khoa</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="flex space-x-1">
              <div className="w-2 h-2 bg-emerald-500 rounded-full animate-bounce [animation-delay:-0.3s]"></div>
              <div className="w-2 h-2 bg-emerald-500 rounded-full animate-bounce [animation-delay:-0.15s]"></div>
              <div className="w-2 h-2 bg-emerald-500 rounded-full animate-bounce"></div>
            </div>
            <span className="text-sm text-muted-foreground ml-2">Đang soạn câu trả lời...</span>
          </div>
        </div>
      </div>
    </div>
  );
}