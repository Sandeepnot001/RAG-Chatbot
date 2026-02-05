import React from 'react';
import { Plus, MessageSquare, Trash2, X } from 'lucide-react';

const ChatSidebar = ({
    sessions,
    currentSessionId,
    onSelectSession,
    onNewChat,
    onDeleteSession,
    isOpen,
    onClose
}) => {
    // Group sessions by date (mock logic for now, or simple list)
    // For MVP, just a flat list sorted by recent.

    return (
        <div className={`
            fixed inset-y-0 left-0 z-40 w-[260px] bg-gray-900 text-gray-100 transform transition-transform duration-300 ease-in-out
            ${isOpen ? 'translate-x-0' : '-translate-x-full'}
            md:relative md:translate-x-0 md:flex md:flex-col
        `}>
            {/* New Chat Button */}
            <div className="p-3">
                <button
                    onClick={onNewChat}
                    className="flex items-center gap-3 w-full px-3 py-3 rounded-md border border-white/20 hover:bg-white/5 transition-colors text-sm text-white mb-2"
                >
                    <Plus size={16} />
                    New chat
                </button>
            </div>

            {/* Scrollable History */}
            <div className="flex-1 overflow-y-auto overflow-x-hidden">
                <div className="px-3 pb-2">
                    <div className="text-xs font-semibold text-gray-500 px-3 py-2">History</div>
                    {sessions.length === 0 && (
                        <div className="px-3 text-sm text-gray-500">No previous chats</div>
                    )}
                    {sessions.slice().reverse().map((session) => (
                        <div
                            key={session.id}
                            className={`
                                group flex items-center gap-3 px-3 py-3 text-sm rounded-md cursor-pointer
                                ${currentSessionId === session.id ? 'bg-white/10' : 'hover:bg-white/5'}
                            `}
                            onClick={() => {
                                onSelectSession(session.id);
                                if (window.innerWidth < 768) onClose(); // Auto close on mobile
                            }}
                        >
                            <MessageSquare size={16} className="text-gray-400" />
                            <div className="flex-1 truncate relative">
                                {session.title || 'New Chat'}
                                <div className="absolute right-0 top-0 bottom-0 w-8 bg-gradient-to-l from-gray-900 to-transparent group-hover:from-[#2A2B32]"></div>
                            </div>
                            {/* Delete Button (visible on hover or active) */}
                            <button
                                onClick={(e) => {
                                    e.stopPropagation();
                                    onDeleteSession(session.id);
                                }}
                                className={`
                                    text-gray-400 hover:text-white p-1 opacity-0 
                                    ${currentSessionId === session.id ? 'opacity-100' : 'group-hover:opacity-100'}
                                    transition-opacity
                                `}
                            >
                                <Trash2 size={14} />
                            </button>
                        </div>
                    ))}
                </div>
            </div>

            {/* User Profile / Footer (Optional) */}
            <div className="p-3 border-t border-white/20">
                <div className="flex items-center gap-3 px-3 py-3 hover:bg-white/5 rounded-md cursor-pointer transition-colors">
                    <div className="h-8 w-8 rounded-sm bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center text-white font-bold text-xs">
                        ST
                    </div>
                    <div className="text-sm font-medium">Student Account</div>
                </div>
            </div>

            {/* Mobile Close Button (Overlay usually handles this, but good to have) */}
            <button
                className="md:hidden absolute top-2 right-[-40px] p-2 bg-gray-900 text-white rounded-r-md"
                onClick={onClose}
            >
                <X size={20} />
            </button>
        </div>
    );
};

export default ChatSidebar;
