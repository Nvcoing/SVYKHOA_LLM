import { useState } from "react";
import { ClaudeSidebar, ChatHistory } from "./ClaudeSidebar";
import { ChatContainer, Chat, Message } from "./ChatContainer";
import { ClaudeWelcome } from "./ClaudeWelcome";
import { SidebarProvider, SidebarTrigger } from "./ui/sidebar";
import { Button } from "./ui/button";
import { Menu } from "lucide-react";
import { API_CONFIG } from "../config";

export function Chat() {
  const [chats, setChats] = useState<Chat[]>([]);
  const [currentChatId, setCurrentChatId] = useState<string | null>(null);

  const currentChat = chats.find(chat => chat.id === currentChatId) || null;

  const generateChatHistory = (): ChatHistory[] => {
    return chats.map(chat => ({
      id: chat.id,
      title: chat.title,
      lastMessage: chat.messages.length > 0 
        ? chat.messages[chat.messages.length - 1].text 
        : "New chat",
      timestamp: chat.updatedAt,
      messageCount: chat.messages.filter(m => m.isUser).length,
    }));
  };

  const handleNewChat = () => {
    const newChat: Chat = {
      id: Date.now().toString(),
      title: "New Chat",
      messages: [],
      createdAt: new Date(),
      updatedAt: new Date(),
    };

    setChats(prev => [newChat, ...prev]);
    setCurrentChatId(newChat.id);
  };

  const handleSelectChat = (chatId: string) => {
    setCurrentChatId(chatId);
  };

  const handleUpdateChat = (updatedChat: Chat) => {
    setChats(prev => prev.map(chat => 
      chat.id === updatedChat.id ? updatedChat : chat
    ));
  };

  const handleDeleteChat = (chatId: string) => {
    setChats(prev => prev.filter(chat => chat.id !== chatId));
    if (currentChatId === chatId) {
      const remainingChats = chats.filter(chat => chat.id !== chatId);
      setCurrentChatId(remainingChats.length > 0 ? remainingChats[0].id : null);
    }
  };

  const handleSendMessage = (messageText: string) => {
    if (!currentChat) {
      // Create a new chat if none exists
      handleNewChat();
      return;
    }

    // This will be handled by ChatContainer
  };

  const handleWelcomeMessage = async (messageText: string) => {
    // Create a new chat and send the message
    const newChat: Chat = {
      id: Date.now().toString(),
      title: messageText.slice(0, 50) + (messageText.length > 50 ? "..." : ""),
      messages: [
        {
          id: Date.now().toString(),
          text: messageText,
          isUser: true,
          timestamp: new Date(),
        }
      ],
      createdAt: new Date(),
      updatedAt: new Date(),
    };

    setChats(prev => [newChat, ...prev]);
    setCurrentChatId(newChat.id);
    
    // Call streaming API
    try {
      const response = await fetch(API_CONFIG.endpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          prompt: messageText 
        }),
      });

      if (!response.ok) {
        // Try to get error details from response
        let errorDetails = '';
        try {
          const errorData = await response.json();
          errorDetails = JSON.stringify(errorData);
          console.error('API error details:', errorData);
        } catch (e) {
          const errorText = await response.text();
          errorDetails = errorText;
          console.error('API error text:', errorText);
        }
        throw new Error(`API error: ${response.status} - ${errorDetails}`);
      }

      // Create initial AI message
      const aiMessageId = (Date.now() + 1).toString();
      const aiMessage: Message = {
        id: aiMessageId,
        text: "",
        isUser: false,
        timestamp: new Date(),
      };

      let aiMessageText = "";
      
      // Read the stream
      const reader = response.body?.getReader();
      const decoder = new TextDecoder();

      if (reader) {
        while (true) {
          const { done, value } = await reader.read();
          
          if (done) break;
          
          // Decode the chunk
          const chunk = decoder.decode(value, { stream: true });
          aiMessageText += chunk;
          
          // Update the AI message with accumulated text
          const updatedAiMessage: Message = {
            ...aiMessage,
            text: aiMessageText,
          };
          
          const streamingChat: Chat = {
            ...newChat,
            messages: [...newChat.messages, updatedAiMessage],
            updatedAt: new Date(),
          };
          
          setChats(prev => prev.map(chat => 
            chat.id === newChat.id ? streamingChat : chat
          ));
        }
      }

    } catch (error) {
      console.error('Error calling API:', error);
      
      // Show error message to user
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: "Sorry, I encountered an error while processing your request. Please try again.",
        isUser: false,
        timestamp: new Date(),
      };
      
      const errorChat: Chat = {
        ...newChat,
        messages: [...newChat.messages, errorMessage],
        updatedAt: new Date(),
      };
      
      setChats(prev => prev.map(chat => 
        chat.id === newChat.id ? errorChat : chat
      ));
    }
  };

  return (
    <SidebarProvider>
      <div className="flex h-screen w-full bg-background">
        <ClaudeSidebar
          chatHistory={generateChatHistory()}
          currentChatId={currentChatId}
          onSelectChat={handleSelectChat}
          onNewChat={handleNewChat}
          onDeleteChat={handleDeleteChat}
        />
        
        <div className="flex-1 flex flex-col overflow-hidden">
          {/* Header with sidebar toggle - Fixed */}
          <div className="flex-shrink-0 flex items-center gap-2 px-4 py-3 border-b border-border bg-white/90 backdrop-blur-sm shadow-sm z-10">
            <SidebarTrigger className="h-8 w-8 p-0 hover:bg-accent">
              <Menu className="h-4 w-4" />
            </SidebarTrigger>
            
            {currentChat && (
              <div className="flex-1 min-w-0">
                <h1 className="text-sm font-medium text-foreground truncate">{currentChat.title}</h1>
              </div>
            )}
          </div>
          
          {/* Main content area */}
          <div className="flex-1 overflow-hidden">
            {currentChat && currentChat.messages.length > 0 ? (
              <ChatContainer
                currentChat={currentChat}
                onUpdateChat={handleUpdateChat}
              />
            ) : (
              <ClaudeWelcome onSendMessage={handleWelcomeMessage} />
            )}
          </div>
        </div>
      </div>
    </SidebarProvider>
  );
}