import React from 'react';
import { Link } from 'react-router-dom';
import { Search, Shield, Zap, FileText, CheckCircle, ArrowRight } from 'lucide-react';

const Home = () => {
    return (
        <div className="min-h-screen">
            {/* Hero Section */}
            <div className="relative overflow-hidden pt-16 pb-32">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
                    <div className="lg:grid lg:grid-cols-12 lg:gap-8 items-center">
                        <div className="lg:col-span-6 text-center lg:text-left animate-slide-up">
                            <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-primary-50 text-primary-600 mb-6 border border-primary-100">
                                <span className="flex h-2 w-2 rounded-full bg-primary-600 mr-2"></span>
                                AI-Powered College Assistant
                            </span>
                            <h1 className="text-4xl tracking-tight font-extrabold text-surface-900 sm:text-5xl md:text-6xl mb-6">
                                <span className="block">Smart Answers from</span>
                                <span className="block bg-clip-text text-transparent bg-gradient-to-r from-primary-600 to-indigo-500">
                                    College Documents
                                </span>
                            </h1>
                            <p className="mt-4 text-lg text-surface-600 mb-8 max-w-2xl mx-auto lg:mx-0">
                                Stop scrolling through endless PDFs. Ask questions in natural language and get instant, verified answers from your syllabus, regulations, and circulars.
                            </p>
                            <div className="flex flex-col sm:flex-row justify-center lg:justify-start gap-4">
                                <Link
                                    to="/chat"
                                    className="btn-primary px-8 py-4 flex items-center justify-center gap-2 text-lg"
                                >
                                    Start Chatting <ArrowRight size={20} />
                                </Link>
                                <Link
                                    to="/admin"
                                    className="px-8 py-4 rounded-lg font-medium text-surface-700 bg-white border border-surface-200 hover:bg-surface-50 hover:border-surface-300 transition-all duration-200 flex items-center justify-center gap-2 shadow-sm"
                                >
                                    Admin Upload <Upload size={20} className="text-surface-500" />
                                </Link>
                            </div>

                            <div className="mt-10 flex items-center justify-center lg:justify-start gap-6 text-surface-500 text-sm">
                                <div className="flex items-center gap-2">
                                    <CheckCircle size={16} className="text-emerald-500" /> <span>Verified Sources</span>
                                </div>
                                <div className="flex items-center gap-2">
                                    <CheckCircle size={16} className="text-emerald-500" /> <span>24/7 Available</span>
                                </div>
                            </div>
                        </div>

                        <div className="lg:col-span-6 mt-16 lg:mt-0 relative animate-fade-in" style={{ animationDelay: '0.2s' }}>
                            {/* Decorative blobs */}
                            <div className="absolute top-0 right-0 -mr-20 -mt-20 w-80 h-80 bg-primary-400/20 rounded-full blur-3xl animate-float"></div>
                            <div className="absolute bottom-0 left-0 -ml-20 -mb-20 w-80 h-80 bg-indigo-400/20 rounded-full blur-3xl animate-float" style={{ animationDelay: '2s' }}></div>

                            {/* 3D-ish Card Stack UI */}
                            <div className="relative mx-auto w-full max-w-md lg:max-w-full">
                                <div className="relative glass-card rounded-2xl p-6 transform rotate-2 hover:rotate-0 transition-transform duration-500 z-20">
                                    <div className="flex items-center gap-3 mb-4 border-b border-surface-100 pb-4">
                                        <div className="h-10 w-10 rounded-full bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center text-white font-bold">S</div>
                                        <div>
                                            <p className="text-sm font-medium text-surface-900">Student</p>
                                            <p className="text-xs text-surface-500">Just now</p>
                                        </div>
                                    </div>
                                    <p className="text-surface-700 font-medium">What are the core subjects for 6th Semester CSE?</p>
                                </div>

                                <div className="relative glass-card rounded-2xl p-6 mt-4 transform -rotate-1 hover:rotate-0 transition-transform duration-500 z-10 translate-x-4">
                                    <div className="flex items-center gap-3 mb-4 border-b border-surface-100 pb-4">
                                        <div className="h-10 w-10 rounded-full bg-gradient-to-br from-emerald-500 to-teal-600 flex items-center justify-center text-white">
                                            <Zap size={20} />
                                        </div>
                                        <div>
                                            <p className="text-sm font-medium text-surface-900">CollegeBot AI</p>
                                            <p className="text-xs text-surface-500">Answered in 1.2s</p>
                                        </div>
                                    </div>
                                    <p className="text-surface-600 text-sm leading-relaxed">
                                        According to the <span className="text-primary-600 font-medium bg-primary-50 px-1 rounded">2021 Regulation Syllabus</span>, the core subjects are:
                                    </p>
                                    <ul className="mt-3 space-y-2 text-sm text-surface-600">
                                        <li className="flex items-center gap-2"><div className="h-1.5 w-1.5 rounded-full bg-primary-500"></div> Compiler Design</li>
                                        <li className="flex items-center gap-2"><div className="h-1.5 w-1.5 rounded-full bg-primary-500"></div> Web Technology</li>
                                        <li className="flex items-center gap-2"><div className="h-1.5 w-1.5 rounded-full bg-primary-500"></div> Artificial Intelligence</li>
                                    </ul>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            {/* Feature Grid */}
            <div className="py-20 relative z-10">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="text-center max-w-3xl mx-auto mb-16">
                        <h2 className="text-primary-600 font-semibold tracking-wide uppercase text-sm">Why Choose CollegeBot</h2>
                        <p className="mt-4 text-3xl font-bold text-surface-900 sm:text-4xl">
                            Unlock the knowledge hidden in your documents
                        </p>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                        {[
                            {
                                icon: <Search className="w-6 h-6 text-white" />,
                                bg: "bg-blue-500",
                                title: "Semantic Search",
                                desc: "Go beyond keywords. Our AI understands the context of your questions to find the most relevant answers."
                            },
                            {
                                icon: <Shield className="w-6 h-6 text-white" />,
                                bg: "bg-emerald-500",
                                title: "Hallucination-Free",
                                desc: "We prioritize accuracy. Answers are strictly derived from uploaded documents with zero AI fabrication."
                            },
                            {
                                icon: <FileText className="w-6 h-6 text-white" />,
                                bg: "bg-purple-500",
                                title: "Source Citations",
                                desc: "Every answer comes with citations. See exactly which document and page page the information was pulled from."
                            }
                        ].map((feature, idx) => (
                            <div key={idx} className="glass-card p-8 rounded-2xl hover:-translate-y-2 transition-transform duration-300">
                                <div className={`h-12 w-12 rounded-xl ${feature.bg} flex items-center justify-center shadow-lg mb-6`}>
                                    {feature.icon}
                                </div>
                                <h3 className="text-xl font-bold text-surface-900 mb-3">{feature.title}</h3>
                                <p className="text-surface-600 leading-relaxed">
                                    {feature.desc}
                                </p>
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        </div>
    );
};

// Helper for upload icon since I used it above but didn't import it in Home (it was in Navbar)
// But wait, I need to make sure Upload is imported or used correctly.
// I'll grab Upload from lucide-react in imports.
import { Upload } from 'lucide-react';

export default Home;
