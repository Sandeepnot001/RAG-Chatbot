import React from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { User, Sparkles, Copy, Check } from 'lucide-react';

const ChatMessage = ({ message }) => {
    const isUser = message.role === 'user';
    const [copied, setCopied] = React.useState(false);

    const handleCopy = () => {
        navigator.clipboard.writeText(message.content);
        setCopied(true);
        setTimeout(() => setCopied(false), 2000);
    };

    return (
        <div className={`group w-full text-surface-800 border-b border-black/5 dark:border-white/5 ${isUser ? 'bg-white' : 'bg-surface-50'}`}>
            <div className="text-base gap-4 md:gap-6 md:max-w-2xl lg:max-w-xl xl:max-w-3xl p-4 md:py-6 flex lg:px-0 m-auto">
                <div className={`flex-shrink-0 flex flex-col relative items-end`}>
                    <div className={`relative h-7 w-7 rounded-sm flex items-center justify-center ${isUser ? 'bg-black text-white' : 'bg-primary-600 text-white'}`}>
                        {isUser ? <User className="h-4 w-4" /> : <Sparkles className="h-4 w-4" />}
                    </div>
                </div>

                <div className="relative flex-1 overflow-hidden" dir="auto">
                    {!isUser && (
                        <div className="font-semibold text-sm mb-1 opacity-90">CollegeBot</div>
                    )}

                    <div className="prose prose-sm md:prose-base dark:prose-invert max-w-none break-words">
                        <ReactMarkdown
                            remarkPlugins={[remarkGfm]}
                            components={{
                                code({ inline, className, children, ...props }) {
                                    return !inline ? (
                                        <div className="bg-gray-900 text-gray-100 rounded-md p-4 my-2 overflow-x-auto">
                                            <code className={className} {...props}>
                                                {children}
                                            </code>
                                        </div>
                                    ) : (
                                        <code className="bg-gray-100 dark:bg-gray-800 rounded px-1 py-0.5" {...props}>
                                            {children}
                                        </code>
                                    )
                                }
                            }}
                        >
                            {message.content}
                        </ReactMarkdown>
                    </div>

                    {/* Sources Section */}
                    {message.sources && message.sources.length > 0 && (
                        <div className="mt-4 pt-2 border-t border-black/5">
                            <div className="text-xs font-semibold text-surface-500 mb-2 uppercase tracking-wide">Sources</div>
                            <div className="flex flex-wrap gap-2">
                                {message.sources.map((source, idx) => (
                                    <span key={idx} className="text-xs bg-surface-200/50 hover:bg-surface-200 text-surface-700 px-2 py-1 rounded transition-colors cursor-default">
                                        {source}
                                    </span>
                                ))}
                            </div>
                        </div>
                    )}

                    {/* Footer / Actions */}
                    {!isUser && (
                        <div className="flex items-center gap-2 mt-2 opacity-0 group-hover:opacity-100 transition-opacity">
                            <button onClick={handleCopy} className="p-1 rounded hover:bg-gray-100 dark:hover:bg-gray-800 text-gray-500">
                                {copied ? <Check size={14} /> : <Copy size={14} />}
                            </button>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default ChatMessage;
