import { useState, useEffect, useRef } from "react";
import { ChatMessage } from "./ChatMessage";
import { ChatInput } from "./ChatInput";
import { TypingIndicator } from "./TypingIndicator";
import { ScrollArea } from "./ui/scroll-area";
import { API_CONFIG } from "../config";

export interface Message {
  id: string;
  text: string;
  isUser: boolean;
  timestamp: Date;
}

export interface Chat {
  id: string;
  title: string;
  messages: Message[];
  createdAt: Date;
  updatedAt: Date;
}

interface ChatContainerProps {
  currentChat: Chat | null;
  onUpdateChat: (chat: Chat) => void;
}

// Mock AI responses for demonstration
const mockResponses = [
  "I'd be happy to help you with that. Let me break this down for you...",
  "That's an interesting question! Based on what you've shared, I think the best approach would be...",
  "I understand your concern. Here's what I would recommend...",
  "Great question! Let me provide you with a comprehensive answer...",
  "I can definitely help with that. Here's my analysis and suggestions...",
  "Thank you for the details. Based on this information, here's what I think...",
  "That's a thoughtful approach. Let me expand on that idea...",
  "I see what you're looking for. Here's how I would tackle this...",
];

export function ChatContainer({ currentChat, onUpdateChat }: ChatContainerProps) {
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [currentChat?.messages, isTyping]);

  const handleSendMessage = async (messageText: string) => {
    if (!currentChat) return;

    // Add user message
    const userMessage: Message = {
      id: Date.now().toString(),
      text: messageText,
      isUser: true,
      timestamp: new Date(),
    };
    
    const updatedMessages = [...currentChat.messages, userMessage];
    
    // Update chat title if this is the first user message after initial
    let updatedTitle = currentChat.title;
    if (currentChat.messages.length <= 1) {
      updatedTitle = messageText.slice(0, 50) + (messageText.length > 50 ? "..." : "");
    }
    
    const updatedChat: Chat = {
      ...currentChat,
      title: updatedTitle,
      messages: updatedMessages,
      updatedAt: new Date(),
    };
    
    onUpdateChat(updatedChat);
    setIsTyping(true);

    try {
      // Call streaming API
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

      setIsTyping(false);

      // Create initial AI message
      const aiMessageId = (Date.now() + 1).toString();
      const aiMessage: Message = {
        id: aiMessageId,
        text: "",
        isUser: false,
        timestamp: new Date(),
      };

      let aiMessageText = "";
      
      // Add the initial empty message
      const chatWithAiMessage: Chat = {
        ...updatedChat,
        messages: [...updatedMessages, aiMessage],
        updatedAt: new Date(),
      };
      onUpdateChat(chatWithAiMessage);

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
            ...updatedChat,
            messages: [...updatedMessages, updatedAiMessage],
            updatedAt: new Date(),
          };
          
          onUpdateChat(streamingChat);
        }
      }

    } catch (error) {
      console.error('Error calling API:', error);
      setIsTyping(false);
      
      // Show error message to user
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: "Sorry, I encountered an error while processing your request. Please try again.",
        isUser: false,
        timestamp: new Date(),
      };
      
      const errorChat: Chat = {
        ...updatedChat,
        messages: [...updatedMessages, errorMessage],
        updatedAt: new Date(),
      };
      
      onUpdateChat(errorChat);
    }
  };

  if (!currentChat) {
    return (
      <div className="flex flex-col items-center justify-center h-full text-center p-8 bg-gradient-to-br from-blue-50 via-white to-emerald-50">
        <div className="max-w-md">
          <h2 className="text-xl mb-4 text-foreground">Chào mừng đến với Trợ lý Y khoa</h2>
          <p className="text-muted-foreground mb-6">
            Bắt đầu cuộc trò chuyện mới từ thanh bên để được tư vấn sức khỏe.
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="flex flex-col h-full overflow-hidden bg-gradient-to-br from-blue-50/30 via-white to-emerald-50/30">
      {/* Messages - Scrollable area */}
      <div className="flex-1 overflow-y-auto">
        <div className="max-w-4xl mx-auto pb-4">
          {currentChat.messages.map((message) => (
            <ChatMessage
              key={message.id}
              message={message.text}
              isUser={message.isUser}
              timestamp={message.timestamp}
            />
          ))}
          {isTyping && <TypingIndicator />}
          <div ref={messagesEndRef} />
        </div>
      </div>

      {/* Input - Fixed at bottom */}
      <div className="flex-shrink-0 p-6 border-t border-border bg-white/90 backdrop-blur-sm shadow-lg">
        <div className="max-w-4xl mx-auto">
          <ChatInput onSendMessage={handleSendMessage} disabled={isTyping} />
        </div>
      </div>
    </div>
  );
}