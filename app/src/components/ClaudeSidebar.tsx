import { useState } from "react";
import { Button } from "./ui/button";
import { ScrollArea } from "./ui/scroll-area";
import { Sidebar, SidebarContent, SidebarHeader, SidebarFooter } from "./ui/sidebar";
import { 
  Plus, 
  MessageSquare, 
  FileText, 
  Stethoscope, 
  Star, 
  Clock,
  ChevronDown,
  User,
  Heart
} from "lucide-react";

export interface ChatHistory {
  id: string;
  title: string;
  lastMessage: string;
  timestamp: Date;
  messageCount: number;
}

interface ClaudeSidebarProps {
  chatHistory: ChatHistory[];
  currentChatId: string | null;
  onSelectChat: (chatId: string) => void;
  onNewChat: () => void;
  onDeleteChat: (chatId: string) => void;
}

export function ClaudeSidebar({ 
  chatHistory, 
  currentChatId, 
  onSelectChat, 
  onNewChat, 
  onDeleteChat 
}: ClaudeSidebarProps) {
  // Mock data for starred and recent items
  const starredItems = [
    "Tư vấn sức khỏe tim mạch",
    "Chế độ dinh dưỡng cho tiểu đường"
  ];

  const recentItems = [
    "Triệu chứng cảm cúm",
    "Thuốc giảm đau an toàn",
    "Chăm sóc sức khỏe trẻ em",
    "Tư vấn dinh dưỡng",
    "Bệnh tiểu đường type 2",
    "Huyết áp cao - Cách kiểm soát",
    "Vitamin và khoáng chất",
    "Stress và sức khỏe tâm thần"
  ];

  const formatTime = (date: Date) => {
    const now = new Date();
    const diff = now.getTime() - date.getTime();
    const days = Math.floor(diff / (1000 * 60 * 60 * 24));
    
    if (days === 0) return "Hôm nay";
    if (days === 1) return "Hôm qua";
    if (days < 7) return `${days} ngày`;
    return date.toLocaleDateString('vi-VN');
  };

  return (
    <Sidebar className="w-64 border-r border-sidebar-border bg-white">
      <SidebarHeader className="p-4 border-b border-sidebar-border bg-gradient-to-r from-blue-50 to-emerald-50">
        <div className="flex items-center gap-2 mb-4">
          <div className="w-8 h-8 bg-emerald-500 rounded-lg flex items-center justify-center shadow-sm">
            <Stethoscope className="text-white h-5 w-5" />
          </div>
          <div>
            <h1 className="font-semibold text-sidebar-foreground">Trợ lý Y khoa</h1>
            <p className="text-xs text-muted-foreground">AI Medical</p>
          </div>
        </div>
        
        <Button 
          onClick={onNewChat} 
          className="w-full justify-start bg-primary hover:bg-primary/90 text-white shadow-sm" 
          size="sm"
        >
          <Plus className="h-4 w-4 mr-2" />
          Cuộc trò chuyện mới
        </Button>
      </SidebarHeader>

      <SidebarContent className="p-0">
        <ScrollArea className="flex-1">
          <div className="p-2">
            {/* Navigation sections */}
            <div className="space-y-1 mb-4">
              <Button
                variant="ghost"
                className="w-full justify-start h-8 px-2 text-sm text-sidebar-foreground/70 hover:bg-blue-50"
              >
                <MessageSquare className="h-4 w-4 mr-2 text-blue-600" />
                Cuộc trò chuyện
              </Button>
              <Button
                variant="ghost"
                className="w-full justify-start h-8 px-2 text-sm text-sidebar-foreground/70 hover:bg-emerald-50"
              >
                <FileText className="h-4 w-4 mr-2 text-emerald-600" />
                Hồ sơ bệnh án
              </Button>
              <Button
                variant="ghost"
                className="w-full justify-start h-8 px-2 text-sm text-sidebar-foreground/70 hover:bg-rose-50"
              >
                <Heart className="h-4 w-4 mr-2 text-rose-600" />
                Sức khỏe
              </Button>
            </div>

            {/* Starred section */}
            <div className="mb-4">
              <div className="flex items-center gap-2 px-2 py-1 text-xs font-medium text-amber-600">
                <Star className="h-3 w-3 fill-amber-500" />
                Đã lưu
              </div>
              <div className="space-y-1 mt-2">
                {starredItems.map((item, index) => (
                  <button
                    key={index}
                    className="w-full text-left px-2 py-1.5 text-sm text-sidebar-foreground hover:bg-blue-50 rounded-md truncate"
                  >
                    {item}
                  </button>
                ))}
              </div>
            </div>

            {/* Recents section */}
            <div>
              <div className="flex items-center gap-2 px-2 py-1 text-xs font-medium text-muted-foreground">
                <Clock className="h-3 w-3" />
                Gần đây
              </div>
              <div className="space-y-1 mt-2">
                {recentItems.map((item, index) => (
                  <button
                    key={index}
                    className="w-full text-left px-2 py-1.5 text-sm text-sidebar-foreground hover:bg-emerald-50 rounded-md truncate"
                    onClick={() => {
                      // For demo purposes, create a new chat when clicking recent items
                      onNewChat();
                    }}
                  >
                    {item}
                  </button>
                ))}
              </div>
            </div>
          </div>
        </ScrollArea>
      </SidebarContent>

      <SidebarFooter className="p-4 border-t border-sidebar-border bg-gradient-to-r from-blue-50 to-emerald-50">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 bg-primary rounded-full flex items-center justify-center shadow-sm">
            <User className="h-4 w-4 text-white" />
          </div>
          <div className="flex-1 min-w-0">
            <p className="text-sm font-medium text-sidebar-foreground">Người dùng</p>
            <p className="text-xs text-emerald-600">● Đang hoạt động</p>
          </div>
          <ChevronDown className="h-4 w-4 text-sidebar-foreground/70" />
        </div>
      </SidebarFooter>
    </Sidebar>
  );
}