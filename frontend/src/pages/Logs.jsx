import React from 'react';
import { ArrowLeft, FileText, AlertCircle, CheckCircle, Clock } from 'lucide-react';
import { Link } from 'react-router-dom';

const Logs = () => {
    // Mock data for now
    const logs = [
        { id: 1, type: 'info', message: 'System startup', time: '09:00 AM', date: new Date().toISOString().split('T')[0] },
        { id: 2, type: 'success', message: 'Vector Database connection established', time: '09:01 AM', date: new Date().toISOString().split('T')[0] },
        { id: 3, type: 'info', message: 'RAG Pipeline initialized', time: '09:01 AM', date: new Date().toISOString().split('T')[0] },
        { id: 4, type: 'success', message: 'System ready for queries', time: '09:02 AM', date: new Date().toISOString().split('T')[0] },
    ];

    return (
        <div className="max-w-7xl mx-auto py-10 px-4 sm:px-6 lg:px-8">
            <div className="mb-8 flex items-center gap-4">
                <Link to="/admin" className="p-2 rounded-lg bg-white border border-surface-200 text-surface-500 hover:text-primary-600 hover:bg-surface-50 transition-colors">
                    <ArrowLeft size={20} />
                </Link>
                <div>
                    <h1 className="text-3xl font-bold text-surface-900 tracking-tight">System Logs</h1>
                    <p className="mt-1 text-surface-500">View system activity and error reports.</p>
                </div>
            </div>

            <div className="glass-panel rounded-2xl overflow-hidden">
                <table className="min-w-full divide-y divide-surface-200">
                    <thead className="bg-surface-50">
                        <tr>
                            <th className="px-6 py-3 text-left text-xs font-medium text-surface-500 uppercase tracking-wider">Status</th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-surface-500 uppercase tracking-wider">Message</th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-surface-500 uppercase tracking-wider">Time</th>
                        </tr>
                    </thead>
                    <tbody className="bg-white divide-y divide-surface-200">
                        {logs.map((log) => (
                            <tr key={log.id} className="hover:bg-surface-50/50 transition-colors">
                                <td className="px-6 py-4 whitespace-nowrap">
                                    <div className="flex items-center">
                                        {log.type === 'success' && <CheckCircle className="text-emerald-500 h-5 w-5" />}
                                        {log.type === 'error' && <AlertCircle className="text-rose-500 h-5 w-5" />}
                                        {log.type === 'info' && <Clock className="text-blue-500 h-5 w-5" />}
                                        <span className={`ml-2 text-sm font-medium capitalize ${log.type === 'success' ? 'text-emerald-700' :
                                            log.type === 'error' ? 'text-rose-700' : 'text-blue-700'
                                            }`}>
                                            {log.type}
                                        </span>
                                    </div>
                                </td>
                                <td className="px-6 py-4">
                                    <div className="text-sm text-surface-900">{log.message}</div>
                                </td>
                                <td className="px-6 py-4 whitespace-nowrap text-sm text-surface-500">
                                    {log.date} • {log.time}
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default Logs;
