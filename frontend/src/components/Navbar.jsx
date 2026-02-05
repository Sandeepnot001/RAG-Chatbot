import React, { useState } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { BookOpen, Monitor, Upload, Home, Menu, X, LogOut, User, Shield, UserPlus } from 'lucide-react';

const Navbar = () => {
    const location = useLocation();
    const navigate = useNavigate();
    const [isOpen, setIsOpen] = useState(false);

    // Get role from localStorage
    const userRole = localStorage.getItem('role');
    const isLoggedIn = !!localStorage.getItem('token');

    const isActive = (path) => {
        return location.pathname === path
            ? 'text-primary-600 bg-primary-50/50'
            : 'text-surface-600 hover:text-primary-600 hover:bg-surface-50/50';
    };

    const handleLogout = () => {
        localStorage.clear();
        setIsOpen(false);
        navigate('/');
        window.location.reload(); // Force reload to clear state
    };

    return (
        <nav className="sticky top-0 z-50 w-full glass-panel border-b border-white/20">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex justify-between h-16">
                    <div className="flex items-center">
                        <Link to="/" className="flex-shrink-0 flex items-center gap-2 group">
                            <div className="h-10 w-10 bg-gradient-to-tr from-primary-600 to-indigo-500 rounded-xl flex items-center justify-center text-white shadow-lg shadow-primary-500/30 group-hover:scale-105 transition-transform duration-300">
                                <BookOpen className="h-6 w-6" />
                            </div>
                            <span className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-primary-700 to-primary-500">
                                CollegeBot
                            </span>
                        </Link>
                    </div>

                    {/* Desktop Menu */}
                    <div className="hidden md:flex space-x-2 items-center">
                        <Link
                            to="/"
                            className={`px-4 py-2 rounded-lg text-sm font-medium flex items-center gap-2 transition-all duration-200 ${isActive('/')}`}
                        >
                            <Home size={18} />
                            Home
                        </Link>

                        {/* Student Link */}
                        {userRole === 'student' && (
                            <Link
                                to="/chat"
                                className={`px-4 py-2 rounded-lg text-sm font-medium flex items-center gap-2 transition-all duration-200 ${isActive('/chat')}`}
                            >
                                <Monitor size={18} />
                                Student Chat
                            </Link>
                        )}

                        {/* Admin Link */}
                        {userRole === 'admin' && (
                            <Link
                                to="/admin"
                                className={`px-4 py-2 rounded-lg text-sm font-medium flex items-center gap-2 transition-all duration-200 ${isActive('/admin')}`}
                            >
                                <Upload size={18} />
                                Admin Portal
                            </Link>
                        )}

                        {!isLoggedIn ? (
                            <>
                                <Link
                                    to="/login/student"
                                    className={`px-4 py-2 rounded-lg text-sm font-medium flex items-center gap-2 transition-all duration-200 ${isActive('/login/student')}`}
                                >
                                    <User size={18} />
                                    Student Login
                                </Link>
                                <Link
                                    to="/login/admin"
                                    className={`px-4 py-2 rounded-lg text-sm font-medium flex items-center gap-2 transition-all duration-200 ${isActive('/login/admin')}`}
                                >
                                    <Shield size={18} />
                                    Admin Login
                                </Link>
                                <Link
                                    to="/register"
                                    className={`px-4 py-2 rounded-lg text-sm font-medium flex items-center gap-2 transition-all duration-200 ${isActive('/register')}`}
                                >
                                    <UserPlus size={18} />
                                    Register
                                </Link>
                            </>
                        ) : (
                            <button
                                onClick={handleLogout}
                                className="ml-2 px-4 py-2 rounded-lg text-sm font-medium flex items-center gap-2 text-red-600 hover:bg-red-50 transition-all duration-200"
                            >
                                <LogOut size={18} />
                                Sign Out
                            </button>
                        )}
                    </div>

                    {/* Mobile menu button */}
                    <div className="flex items-center md:hidden">
                        <button
                            onClick={() => setIsOpen(!isOpen)}
                            className="p-2 rounded-md text-surface-600 hover:text-primary-600 hover:bg-surface-100 focus:outline-none"
                        >
                            {isOpen ? <X size={24} /> : <Menu size={24} />}
                        </button>
                    </div>
                </div>
            </div>

            {/* Mobile Menu */}
            {isOpen && (
                <div className="md:hidden glass-panel border-t border-white/20 animate-fade-in absolute w-full backdrop-blur-xl">
                    <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3">
                        <Link
                            to="/"
                            onClick={() => setIsOpen(false)}
                            className={`block px-3 py-2 rounded-md text-base font-medium flex items-center gap-2 ${isActive('/')}`}
                        >
                            <Home size={18} /> Home
                        </Link>

                        {userRole === 'student' && (
                            <Link
                                to="/chat"
                                onClick={() => setIsOpen(false)}
                                className={`block px-3 py-2 rounded-md text-base font-medium flex items-center gap-2 ${isActive('/chat')}`}
                            >
                                <Monitor size={18} /> Student Chat
                            </Link>
                        )}

                        {userRole === 'admin' && (
                            <Link
                                to="/admin"
                                onClick={() => setIsOpen(false)}
                                className={`block px-3 py-2 rounded-md text-base font-medium flex items-center gap-2 ${isActive('/admin')}`}
                            >
                                <Upload size={18} /> Admin Portal
                            </Link>
                        )}

                        {!isLoggedIn ? (
                            <>
                                <Link
                                    to="/login/student"
                                    onClick={() => setIsOpen(false)}
                                    className={`block px-3 py-2 rounded-md text-base font-medium flex items-center gap-2 ${isActive('/login/student')}`}
                                >
                                    <User size={18} /> Student Login
                                </Link>
                                <Link
                                    to="/login/admin"
                                    onClick={() => setIsOpen(false)}
                                    className={`block px-3 py-2 rounded-md text-base font-medium flex items-center gap-2 ${isActive('/login/admin')}`}
                                >
                                    <Shield size={18} /> Admin Login
                                </Link>
                                <Link
                                    to="/register"
                                    onClick={() => setIsOpen(false)}
                                    className={`block px-3 py-2 rounded-md text-base font-medium flex items-center gap-2 ${isActive('/register')}`}
                                >
                                    <UserPlus size={18} /> Register
                                </Link>
                            </>
                        ) : (
                            <button
                                onClick={handleLogout}
                                className="w-full text-left block px-3 py-2 rounded-md text-base font-medium flex items-center gap-2 text-red-600 hover:bg-red-50"
                            >
                                <LogOut size={18} /> Sign Out
                            </button>
                        )}
                    </div>
                </div>
            )}
        </nav>
    );
};

export default Navbar;
