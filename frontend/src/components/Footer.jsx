import React from 'react';

const Footer = () => {
    return (
        <footer className="bg-white border-t border-surface-200 py-8 mt-auto">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col md:flex-row justify-between items-center gap-4">
                <div className="text-center md:text-left">
                    <p className="text-sm text-surface-500">
                        &copy; {new Date().getFullYear()} <span className="font-semibold text-surface-700">CollegeBot</span>. All rights reserved.
                    </p>
                    <p className="text-xs text-surface-400 mt-1">
                        AI-Powered Academic Assistant
                    </p>
                </div>
                <div className="flex gap-6 text-sm text-surface-500">
                    <a href="#" className="hover:text-primary-600 transition-colors">Privacy Policy</a>
                    <a href="#" className="hover:text-primary-600 transition-colors">Terms of Service</a>
                    <a href="#" className="hover:text-primary-600 transition-colors">Contact Support</a>
                </div>
            </div>
        </footer>
    );
};

export default Footer;
