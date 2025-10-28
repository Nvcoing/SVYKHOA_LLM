import { Button } from "./ui/button";
import { Textarea } from "./ui/textarea";
import { useState } from "react";
import { 
  Stethoscope,
  Heart,
  Pill,
  Activity,
  FileText,
  Thermometer,
  Send,
  Sparkles
} from "lucide-react";

interface ClaudeWelcomeProps {
  onSendMessage: (message: string) => void;
  userName?: string;
}

export function ClaudeWelcome({ onSendMessage, userName = "Bệnh nhân" }: ClaudeWelcomeProps) {
  const [inputValue, setInputValue] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (inputValue.trim()) {
      onSendMessage(inputValue.trim());
      setInputValue("");
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  const actionButtons = [
    { icon: Stethoscope, label: "Chẩn đoán", color: "bg-blue-500/10 text-blue-600 border-blue-500/30 hover:bg-blue-500/20" },
    { icon: Pill, label: "Tư vấn thuốc", color: "bg-emerald-500/10 text-emerald-600 border-emerald-500/30 hover:bg-emerald-500/20" },
    { icon: Activity, label: "Triệu chứng", color: "bg-purple-500/10 text-purple-600 border-purple-500/30 hover:bg-purple-500/20" },
    { icon: Heart, label: "Sức khỏe", color: "bg-rose-500/10 text-rose-600 border-rose-500/30 hover:bg-rose-500/20" },
    { icon: FileText, label: "Hồ sơ bệnh án", color: "bg-amber-500/10 text-amber-600 border-amber-500/30 hover:bg-amber-500/20" },
  ];

  return (
    <div className="flex flex-col h-full overflow-hidden bg-gradient-to-br from-blue-50 via-white to-emerald-50">
      {/* Header notification */}
      <div className="flex-shrink-0 flex justify-center p-4 bg-white/80 backdrop-blur-sm border-b border-border">
        <div className="flex items-center gap-2 text-sm text-muted-foreground">
          <Thermometer className="h-4 w-4 text-primary" />
          <span>Trợ lý Y khoa - Hỗ trợ tư vấn sức khỏe 24/7</span>
        </div>
      </div>

      {/* Main content - Scrollable */}
      <div className="flex-1 overflow-y-auto flex flex-col items-center justify-center px-8 max-w-3xl mx-auto w-full">
        {/* Welcome message */}
        <div className="text-center mb-12">
          <div className="flex items-center justify-center gap-3 mb-4">
            <div className="p-3 bg-emerald-500 rounded-full">
              <Stethoscope className="h-8 w-8 text-white" />
            </div>
          </div>
          <h1 className="text-3xl text-foreground mb-2">Xin chào!</h1>
          <p className="text-muted-foreground">Tôi có thể giúp gì cho bạn hôm nay?</p>
        </div>

        {/* Input area */}
        <div className="w-full max-w-2xl">
          <form onSubmit={handleSubmit} className="relative mb-8">
            <Textarea
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Hãy mô tả triệu chứng hoặc câu hỏi của bạn..."
              className="min-h-[80px] pr-12 bg-white border-2 border-border hover:border-primary/50 focus:border-primary resize-none shadow-sm"
            />
            <Button
              type="submit"
              size="sm"
              className="absolute bottom-3 right-3 h-9 w-9 p-0 bg-primary hover:bg-primary/90"
              disabled={!inputValue.trim()}
            >
              <Send className="h-4 w-4" />
            </Button>
          </form>

          {/* Action buttons */}
          <div className="flex flex-wrap gap-3 justify-center">
            {actionButtons.map((action, index) => {
              const IconComponent = action.icon;
              return (
                <Button
                  key={index}
                  variant="outline"
                  size="sm"
                  className={`${action.color} shadow-sm`}
                  onClick={() => onSendMessage(`Tôi cần ${action.label.toLowerCase()}`)}
                >
                  <IconComponent className="h-4 w-4 mr-2" />
                  {action.label}
                </Button>
              );
            })}
          </div>
          
          {/* Disclaimer */}
          <div className="mt-8 p-4 bg-amber-50 border border-amber-200 rounded-lg">
            <p className="text-xs text-amber-900 text-center">
              ⚠️ <strong>Lưu ý:</strong> Đây chỉ là công cụ hỗ trợ tham khảo. Vui lòng tham khảo ý kiến bác sĩ chuyên khoa để có chẩn đoán và điều trị chính xác.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}