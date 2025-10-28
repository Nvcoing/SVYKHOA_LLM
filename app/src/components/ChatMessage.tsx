import { Avatar, AvatarFallback } from "./ui/avatar";
import { User, Stethoscope } from "lucide-react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import rehypeRaw from "rehype-raw";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { oneLight } from "react-syntax-highlighter/dist/esm/styles/prism";

interface ChatMessageProps {
  message: string;
  isUser: boolean;
  timestamp: Date;
}

export function ChatMessage({ message, isUser, timestamp }: ChatMessageProps) {
  return (
    <div className={`px-6 py-6 border-b border-border ${isUser ? "bg-white" : "bg-accent/30"}`}>
      <div className="flex gap-4 max-w-none">
        <Avatar className="h-9 w-9 flex-shrink-0 border-2 border-border">
          <AvatarFallback className={isUser ? "bg-primary text-primary-foreground" : "bg-emerald-500 text-white"}>
            {isUser ? <User className="h-4 w-4" /> : <Stethoscope className="h-4 w-4" />}
          </AvatarFallback>
        </Avatar>
        
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 mb-3">
            <span className="font-medium text-foreground">
              {isUser ? "Bạn" : "Trợ lý Y khoa"}
            </span>
            <span className="text-xs text-muted-foreground">
              {timestamp.toLocaleTimeString('vi-VN', { hour: '2-digit', minute: '2-digit' })}
            </span>
          </div>
          <div className="text-foreground prose prose-slate max-w-none prose-pre:p-0 prose-pre:m-0 prose-pre:bg-transparent prose-headings:text-foreground prose-p:text-foreground prose-strong:text-foreground prose-li:text-foreground prose-a:text-primary">
            {isUser ? (
              <div className="whitespace-pre-wrap break-words leading-relaxed">
                {message}
              </div>
            ) : (
              <ReactMarkdown
                remarkPlugins={[remarkGfm]}
                rehypePlugins={[rehypeRaw]}
                components={{
                  code({ node, inline, className, children, ...props }: any) {
                    const match = /language-(\w+)/.exec(className || '');
                    return !inline && match ? (
                      <SyntaxHighlighter
                        style={oneLight}
                        language={match[1]}
                        PreTag="div"
                        customStyle={{
                          margin: '1em 0',
                          borderRadius: '0.5rem',
                          fontSize: '0.875rem',
                          border: '1px solid #e5e7eb',
                        }}
                        {...props}
                      >
                        {String(children).replace(/\n$/, '')}
                      </SyntaxHighlighter>
                    ) : (
                      <code className="bg-accent px-2 py-0.5 rounded text-sm border border-border" {...props}>
                        {children}
                      </code>
                    );
                  },
                  answer({ children }: any) {
                    return (
                      <div className="my-4 p-4 bg-emerald-50 border-l-4 border-emerald-500 rounded-r-lg">
                        <div className="flex items-start gap-2">
                          <Stethoscope className="h-5 w-5 text-emerald-600 flex-shrink-0 mt-0.5" />
                          <div className="flex-1 text-emerald-900">
                            {children}
                          </div>
                        </div>
                      </div>
                    );
                  },
                  p({ children }) {
                    return <p className="mb-4 last:mb-0 leading-relaxed">{children}</p>;
                  },
                  ul({ children }) {
                    return <ul className="list-disc pl-6 mb-4 space-y-1">{children}</ul>;
                  },
                  ol({ children }) {
                    return <ol className="list-decimal pl-6 mb-4 space-y-1">{children}</ol>;
                  },
                  li({ children }) {
                    return <li className="leading-relaxed">{children}</li>;
                  },
                  h1({ children }) {
                    return <h1 className="mb-4 mt-6 first:mt-0">{children}</h1>;
                  },
                  h2({ children }) {
                    return <h2 className="mb-3 mt-5 first:mt-0">{children}</h2>;
                  },
                  h3({ children }) {
                    return <h3 className="mb-2 mt-4 first:mt-0">{children}</h3>;
                  },
                  blockquote({ children }) {
                    return (
                      <blockquote className="border-l-4 border-primary/30 pl-4 italic my-4 text-muted-foreground bg-muted/50 py-2 rounded-r">
                        {children}
                      </blockquote>
                    );
                  },
                  a({ children, href }) {
                    return (
                      <a
                        href={href}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-primary hover:text-primary/80 underline decoration-primary/30 hover:decoration-primary"
                      >
                        {children}
                      </a>
                    );
                  },
                  table({ children }) {
                    return (
                      <div className="my-4 overflow-x-auto">
                        <table className="min-w-full border-collapse border border-border">
                          {children}
                        </table>
                      </div>
                    );
                  },
                  th({ children }) {
                    return (
                      <th className="border border-border px-4 py-2 bg-muted/50 text-left">
                        {children}
                      </th>
                    );
                  },
                  td({ children }) {
                    return <td className="border border-border px-4 py-2">{children}</td>;
                  },
                }}
              >
                {message}
              </ReactMarkdown>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}