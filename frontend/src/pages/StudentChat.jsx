import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import { Send, Menu, Loader } from 'lucide-react';
import ChatSidebar from '../components/ChatSidebar';
import ChatMessage from '../components/ChatMessage';
import { API_BASE_URL } from '../apiConfig';

const StudentChat = () => {
    // Session Management
    const [sessions, setSessions] = useState(() => {
        const saved = localStorage.getItem('chatSessions');
        return saved ? JSON.parse(saved) : [];
    });
    const [currentSessionId, setCurrentSessionId] = useState(null);
    const [sidebarOpen, setSidebarOpen] = useState(false);

    // Chat State
    const [query, setQuery] = useState('');
    const [loading, setLoading] = useState(false);
    const messagesEndRef = useRef(null);

    // Persist sessions
    useEffect(() => {
        localStorage.setItem('chatSessions', JSON.stringify(sessions));
    }, [sessions]);

    // Scroll to bottom
    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    }, [sessions, currentSessionId, loading]);

    // Helper: Generate ID
    const generateId = () => Date.now().toString(36) + Math.random().toString(36).substr(2);

    const getCurrentMessages = () => {
        const session = sessions.find(s => s.id === currentSessionId);
        return session ? session.messages : [];
    };

    const handleNewChat = () => {
        setCurrentSessionId(null);
        setSidebarOpen(false); // Close sidebar on mobile
    };

    const handleDeleteSession = (id) => {
        setSessions(prev => prev.filter(s => s.id !== id));
        if (currentSessionId === id) {
            setCurrentSessionId(null);
        }
    };

    const handleSend = async (e) => {
        e.preventDefault();
        if (!query.trim()) return;

        let activeSessionId = currentSessionId;
        const timestamp = Date.now();

        // Create new session if none exists
        if (!activeSessionId) {
            const newId = generateId();
            const newSession = {
                id: newId,
                title: query.length > 30 ? query.substring(0, 30) + '...' : query, // Simple title generation
                timestamp: timestamp,
                messages: []
            };
            setSessions(prev => [...prev, newSession]);
            activeSessionId = newId;
            setCurrentSessionId(newId);
        }

        // Add User Message
        const userMessage = { role: 'user', content: query, sources: [], time: null };
        setQuery('');
        setLoading(true);

        setSessions(prev => prev.map(s => {
            if (s.id === activeSessionId) {
                return { ...s, messages: [...s.messages, userMessage] };
            }
            return s;
        }));

        try {
            const token = localStorage.getItem('token');
            const headers = token ? { Authorization: `Bearer ${token}` } : {};

            const response = await axios.post(`${API_BASE_URL}/api/chat`, { question: userMessage.content }, { headers });
            const botMessage = {
                role: 'assistant',
                content: response.data.answer,
                sources: response.data.sources || [],
                time: null // API doesn't return time in this updated flow usually, or we calculate it
            };

            setSessions(prev => prev.map(s => {
                if (s.id === activeSessionId) {
                    return { ...s, messages: [...s.messages, botMessage] };
                }
                return s;
            }));

        } catch (error) {
            console.error("Error:", error);
            let content = 'Sorry, I encountered an error connecting to the server. Please check if the backend is running.';

            if (error.response && error.response.status === 401) {
                content = 'Your session has expired or you are not logged in. Redirecting to login...';
                setTimeout(() => window.location.href = '/', 2000); // Redirect to home/login
            }

            const errorMessage = {
                role: 'assistant',
                content: content,
                sources: []
            };
            setSessions(prev => prev.map(s => {
                if (s.id === activeSessionId) {
                    return { ...s, messages: [...s.messages, errorMessage] };
                }
                return s;
            }));
        } finally {
            setLoading(false);
        }
    };

    const currentMessages = getCurrentMessages();

    return (
        <div className="flex h-[calc(100vh-4rem)] overflow-hidden bg-white dark:bg-gray-800">
            {/* Sidebar */}
            <ChatSidebar
                sessions={sessions}
                currentSessionId={currentSessionId}
                onSelectSession={setCurrentSessionId}
                onNewChat={handleNewChat}
                onDeleteSession={handleDeleteSession}
                isOpen={sidebarOpen}
                onClose={() => setSidebarOpen(false)}
            />

            {/* Main Chat Area */}
            <div className="flex-1 flex flex-col relative w-full h-full">

                {/* Mobile Header */}
                <div className="md:hidden flex items-center p-4 border-b border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 z-10">
                    <button onClick={() => setSidebarOpen(true)} className="p-2 -ml-2 text-gray-600 dark:text-gray-300">
                        <Menu size={24} />
                    </button>
                    <span className="font-semibold ml-2 text-gray-700 dark:text-gray-200">CollegeBot</span>
                </div>

                {/* Messages */}
                <div className="flex-1 overflow-y-auto scroll-smooth">
                    {currentMessages.length === 0 ? (
                        <div className="flex flex-col items-center justify-center h-full px-4 text-center">
                            <div className="bg-white dark:bg-gray-700 p-4 rounded-full shadow-sm mb-6">
                                <div className="h-12 w-12 bg-primary-600 rounded-2xl flex items-center justify-center">
                                    <Send className="text-white h-6 w-6" />
                                </div>
                            </div>
                            <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">How can I help you today?</h2>
                            <p className="text-gray-500 dark:text-gray-400 max-w-md">
                                Ask about your syllabus, regulations, circulars, or any college-related queries.
                            </p>
                        </div>
                    ) : (
                        <div className="flex flex-col pb-32">
                            {currentMessages.map((msg, idx) => (
                                <ChatMessage key={idx} message={msg} />
                            ))}
                            {loading && (
                                <div className="p-4 md:py-6 max-w-2xl lg:max-w-xl xl:max-w-3xl m-auto w-full flex gap-4">
                                    <div className="h-7 w-7 bg-primary-600 rounded-sm flex items-center justify-center flex-shrink-0">
                                        <Loader className="animate-spin text-white h-4 w-4" />
                                    </div>
                                    <div className="flex items-center">
                                        <span className="text-gray-500 text-sm animate-pulse">Thinking...</span>
                                    </div>
                                </div>
                            )}
                            <div ref={messagesEndRef} />
                        </div>
                    )}
                </div>

                {/* Input Area */}
                <div className="absolute bottom-0 left-0 w-full bg-gradient-to-t from-white via-white to-transparent dark:from-gray-800 dark:via-gray-800 pt-10 pb-6 px-4">
                    <div className="max-w-2xl lg:max-w-xl xl:max-w-3xl mx-auto">
                        <form onSubmit={handleSend} className="relative shadow-lg rounded-xl dark:shadow-none">
                            <input
                                type="text"
                                className="w-full bg-white dark:bg-gray-700 border border-gray-200 dark:border-gray-600 text-gray-900 dark:text-white rounded-xl pl-4 pr-12 py-4 focus:ring-2 focus:ring-primary-500 focus:border-transparent shadow-sm placeholder-gray-400"
                                placeholder="Message CollegeBot..."
                                value={query}
                                onChange={(e) => setQuery(e.target.value)}
                                disabled={loading}
                            />
                            <button
                                type="submit"
                                disabled={loading || !query.trim()}
                                className="absolute right-2 top-1/2 -translate-y-1/2 p-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 disabled:opacity-50 disabled:hover:bg-primary-600 transition-colors"
                            >
                                <Send className="h-4 w-4" />
                            </button>
                        </form>
                        <p className="text-center text-xs text-gray-400 dark:text-gray-500 mt-2">
                            CollegeBot can make mistakes. Verify important info.
                        </p>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default StudentChat;

