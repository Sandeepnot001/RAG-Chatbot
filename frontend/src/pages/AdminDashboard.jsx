import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Upload, CheckCircle, AlertCircle, FileText, BarChart3, Users, Database, Trash2 } from 'lucide-react';
import { Link } from 'react-router-dom';
import ReactMarkdown from 'react-markdown';

const AdminDashboard = () => {
    const [file, setFile] = useState(null);
    const [department, setDepartment] = useState('');
    const [semester, setSemester] = useState('');
    const [uploading, setUploading] = useState(false);
    const [status, setStatus] = useState(null);
    const [summary, setSummary] = useState(null);
    const [stats, setStats] = useState({
        total_documents: 0,
        active_students: 0,
        queries_today: 0
    });
    const [documents, setDocuments] = useState([]);

    const departments = ["Computer Science", "Electronics", "Mechanical", "Civil", "MBA"];
    const semesters = ["Semester 1", "Semester 2", "Semester 3", "Semester 4", "Semester 5", "Semester 6", "Semester 7", "Semester 8"];

    const getAuthHeader = () => {
        const token = localStorage.getItem('token');
        return token ? { Authorization: `Bearer ${token}` } : {};
    };

    useEffect(() => {
        fetchStats();
        fetchDocuments();
    }, []);

    const fetchStats = async () => {
        try {
            const response = await axios.get('/api/stats', { headers: getAuthHeader() });
            setStats(response.data);
        } catch (error) {
            console.error("Failed to fetch stats", error);
            if (error.response && error.response.status === 401) {
                window.location.href = '/login/admin';
            }
        }
    };

    const fetchDocuments = async () => {
        try {
            const response = await axios.get('/api/documents', { headers: getAuthHeader() });
            if (response.data && response.data.documents) {
                setDocuments(response.data.documents);
            }
        } catch (error) {
            console.error("Failed to fetch documents", error);
            if (error.response && error.response.status === 401) {
                window.location.href = '/login/admin';
            }
        }
    };

    const handleFileChange = (e) => {
        if (e.target.files) {
            setFile(e.target.files[0]);
            setStatus(null);
            setSummary(null);
        }
    };

    const handleUpload = async (e) => {
        e.preventDefault();
        if (!file || !department || !semester) {
            setStatus({ type: 'error', message: 'Please select file, department, and semester.' });
            return;
        }

        setUploading(true);
        setStatus(null);
        setSummary(null);

        const formData = new FormData();
        formData.append('file', file);
        formData.append('department', department);
        formData.append('semester', semester);

        try {
            const response = await axios.post('/api/upload', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                    ...getAuthHeader()
                },
            });
            setStatus({ type: 'success', message: `Successfully uploaded ${file.name}` });
            if (response.data.summary) {
                setSummary(response.data.summary);
            }
            setFile(null);
            setDepartment('');
            setSemester('');
            // Refresh data
            fetchStats();
            fetchDocuments();
        } catch (error) {
            console.error("Upload failed", error);
            setStatus({ type: 'error', message: 'Failed to upload document.' });
        } finally {
            setUploading(false);
        }
    };

    const handleDelete = async (filename) => {
        if (!window.confirm(`Are you sure you want to delete ${filename}?`)) return;

        try {
            await axios.delete(`/api/documents/${filename}`, {
                headers: getAuthHeader()
            });
            setStatus({ type: 'success', message: `Deleted ${filename}` });
            fetchDocuments(); // Refresh list
            fetchStats(); // Refresh stats
        } catch (error) {
            console.error("Delete failed", error);
            setStatus({ type: 'error', message: 'Failed to delete document.' });
        }
    };

    return (
        <div className="max-w-7xl mx-auto py-10 px-4 sm:px-6 lg:px-8">
            <div className="mb-10 flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div>
                    <h1 className="text-3xl font-bold text-surface-900 tracking-tight">Admin Dashboard</h1>
                    <p className="mt-1 text-surface-500">Manage knowledge base and monitor system status.</p>
                </div>
                <div className="flex gap-3">
                    <Link to="/admin/logs" className="px-4 py-2 bg-white border border-surface-200 rounded-lg text-sm font-medium text-surface-600 shadow-sm hover:bg-surface-50 transition-colors">View Logs</Link>
                    <Link to="/admin/settings" className="px-4 py-2 bg-primary-600 text-white rounded-lg text-sm font-medium shadow-lg shadow-primary-500/20 hover:bg-primary-700 transition-colors">Settings</Link>
                </div>
            </div>

            {/* Stats Cards */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-10">
                <div className="glass-card p-6 rounded-2xl flex items-center gap-4">
                    <div className="h-12 w-12 rounded-xl bg-blue-100 text-blue-600 flex items-center justify-center">
                        <Database size={24} />
                    </div>
                    <div>
                        <p className="text-sm font-medium text-surface-500">Total Documents</p>
                        <p className="text-2xl font-bold text-surface-900">{stats.total_documents}</p>
                    </div>
                </div>
                <div className="glass-card p-6 rounded-2xl flex items-center gap-4">
                    <div className="h-12 w-12 rounded-xl bg-emerald-100 text-emerald-600 flex items-center justify-center">
                        <Users size={24} />
                    </div>
                    <div>
                        <p className="text-sm font-medium text-surface-500">Active Students</p>
                        <p className="text-2xl font-bold text-surface-900">{stats.active_students}</p>
                    </div>
                </div>
                <div className="glass-card p-6 rounded-2xl flex items-center gap-4">
                    <div className="h-12 w-12 rounded-xl bg-purple-100 text-purple-600 flex items-center justify-center">
                        <BarChart3 size={24} />
                    </div>
                    <div>
                        <p className="text-sm font-medium text-surface-500">Queries Today</p>
                        <p className="text-2xl font-bold text-surface-900">{stats.queries_today}</p>
                    </div>
                </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                {/* Upload Section */}
                <div className="glass-panel rounded-2xl p-8">
                    <h2 className="text-xl font-semibold text-surface-900 mb-6 flex items-center gap-2">
                        <Upload className="text-primary-600" size={20} /> Upload New Document
                    </h2>

                    <form onSubmit={handleUpload} className="space-y-6">
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                            <div>
                                <label className="block text-sm font-medium text-surface-700 mb-1">Department</label>
                                <select
                                    value={department}
                                    onChange={(e) => setDepartment(e.target.value)}
                                    className="w-full px-4 py-2 bg-white border border-surface-200 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent outline-none transition-all"
                                    required
                                >
                                    <option value="">Select Department</option>
                                    {departments.map(dept => (
                                        <option key={dept} value={dept}>{dept}</option>
                                    ))}
                                </select>
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-surface-700 mb-1">Semester</label>
                                <select
                                    value={semester}
                                    onChange={(e) => setSemester(e.target.value)}
                                    className="w-full px-4 py-2 bg-white border border-surface-200 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent outline-none transition-all"
                                    required
                                >
                                    <option value="">Select Semester</option>
                                    {semesters.map(sem => (
                                        <option key={sem} value={sem}>{sem}</option>
                                    ))}
                                </select>
                            </div>
                        </div>

                        <div className={`border-2 border-dashed rounded-xl p-10 text-center transition-all duration-200 ${file ? 'border-primary-500 bg-primary-50/50' : 'border-surface-300 hover:border-primary-400 hover:bg-surface-50'}`}>
                            <div className="space-y-3">
                                {!file ? (
                                    <>
                                        <div className="mx-auto h-12 w-12 text-surface-400 bg-surface-100 rounded-full flex items-center justify-center">
                                            <Upload size={24} />
                                        </div>
                                        <div className="flex text-sm text-surface-600 justify-center">
                                            <label htmlFor="file-upload" className="relative cursor-pointer font-medium text-primary-600 hover:text-primary-500">
                                                <span>Click to upload</span>
                                                <input id="file-upload" name="file-upload" type="file" className="sr-only" onChange={handleFileChange} accept=".pdf,.txt,.docx" />
                                            </label>
                                            <p className="pl-1">or drag and drop</p>
                                        </div>
                                        <p className="text-xs text-surface-500">PDF, DOCX, TXT up to 10MB</p>
                                    </>
                                ) : (
                                    <div className="flex flex-col items-center animate-fade-in">
                                        <div className="h-12 w-12 bg-primary-100 text-primary-600 rounded-xl flex items-center justify-center mb-2">
                                            <FileText size={24} />
                                        </div>
                                        <p className="text-sm font-medium text-surface-900">{file.name}</p>
                                        <p className="text-xs text-surface-500">{(file.size / 1024 / 1024).toFixed(2)} MB</p>
                                        <button onClick={() => setFile(null)} className="mt-2 text-xs text-red-500 hover:text-red-600 font-medium">Remove</button>
                                    </div>
                                )}
                            </div>
                        </div>

                        <div className="flex justify-end">
                            <button
                                type="submit"
                                disabled={!file || uploading}
                                className="btn-primary px-6 py-2.5 disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
                            >
                                {uploading ? (
                                    <>
                                        <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                                        Processing...
                                    </>
                                ) : (
                                    <>Upload Document</>
                                )}
                            </button>
                        </div>
                    </form>

                    {status && (
                        <div className={`mt-6 p-4 rounded-xl flex items-start gap-3 animate-fade-in ${status.type === 'success' ? 'bg-emerald-50 border border-emerald-100' : 'bg-rose-50 border border-rose-100'}`}>
                            {status.type === 'success' ? (
                                <CheckCircle className="h-5 w-5 text-emerald-500 flex-shrink-0" />
                            ) : (
                                <AlertCircle className="h-5 w-5 text-rose-500 flex-shrink-0" />
                            )}
                            <div>
                                <h3 className={`text-sm font-medium ${status.type === 'success' ? 'text-emerald-800' : 'text-rose-800'}`}>
                                    {status.type === 'success' ? 'Upload Successful' : 'Upload Failed'}
                                </h3>
                                <p className={`mt-1 text-sm ${status.type === 'success' ? 'text-emerald-600' : 'text-rose-600'}`}>
                                    {status.message}
                                </p>
                            </div>
                        </div>
                    )}
                </div>

                {summary && (
                    <div className="glass-panel rounded-xl p-6 mt-6 animate-fade-in border-l-4 border-indigo-500 bg-indigo-50/50">
                        <h3 className="text-lg font-semibold text-indigo-900 mb-2 flex items-center gap-2">
                            <FileText className="h-5 w-5" /> Document Summary
                        </h3>
                        <div className="prose prose-sm text-indigo-800">
                            <ReactMarkdown>{summary}</ReactMarkdown>
                        </div>
                    </div>
                )}

                {/* Recent Files Mockup -> Real Data */}
                <div className="glass-panel rounded-2xl p-8">
                    <h2 className="text-xl font-semibold text-surface-900 mb-6">Recent Documents</h2>
                    <div className="overflow-hidden rounded-xl border border-surface-200">
                        <table className="min-w-full divide-y divide-surface-200">
                            <thead className="bg-surface-50">
                                <tr>
                                    <th className="px-6 py-3 text-left text-xs font-medium text-surface-500 uppercase tracking-wider">Name</th>
                                    <th className="px-6 py-3 text-left text-xs font-medium text-surface-500 uppercase tracking-wider">Dept / Sem</th>
                                    <th className="px-6 py-3 text-right text-xs font-medium text-surface-500 uppercase tracking-wider">Actions</th>
                                </tr>
                            </thead>
                            <tbody className="bg-white divide-y divide-surface-200">
                                {documents.length > 0 ? (
                                    documents.map((doc, index) => (
                                        <tr key={index}>
                                            <td className="px-6 py-4 whitespace-nowrap">
                                                <div className="flex items-center gap-3">
                                                    <FileText size={18} className="text-surface-400" />
                                                    <span className="text-sm font-medium text-surface-900">{doc.name}</span>
                                                </div>
                                            </td>
                                            <td className="px-6 py-4 whitespace-nowrap">
                                                <div className="text-sm text-surface-600">
                                                    <span className="block">{doc.department}</span>
                                                    <span className="text-xs text-surface-400">{doc.semester}</span>
                                                </div>
                                            </td>
                                            <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                                                <button
                                                    onClick={() => handleDelete(doc.name)}
                                                    className="text-red-600 hover:text-red-900 transition-colors p-2 hover:bg-red-50 rounded-lg"
                                                    title="Delete Document"
                                                >
                                                    <Trash2 size={18} />
                                                </button>
                                            </td>
                                        </tr>
                                    ))
                                ) : (
                                    <tr>
                                        <td colSpan="3" className="px-6 py-4 text-center text-sm text-surface-500">No documents found.</td>
                                    </tr>
                                )}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default AdminDashboard;
