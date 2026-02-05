import React, { useState } from 'react';
import { ArrowLeft, Save, Shield, Database, Bell } from 'lucide-react';
import { Link } from 'react-router-dom';

const Settings = () => {
    const [config, setConfig] = useState({
        systemName: 'CollegeBot AI',
        maintenanceMode: false,
        logLevel: 'Info',
        maxTokens: 512
    });

    const handleChange = (e) => {
        const { name, value, type, checked } = e.target;
        setConfig(prev => ({
            ...prev,
            [name]: type === 'checkbox' ? checked : value
        }));
    };

    return (
        <div className="max-w-4xl mx-auto py-10 px-4 sm:px-6 lg:px-8">
            <div className="mb-8 flex items-center gap-4">
                <Link to="/admin" className="p-2 rounded-lg bg-white border border-surface-200 text-surface-500 hover:text-primary-600 hover:bg-surface-50 transition-colors">
                    <ArrowLeft size={20} />
                </Link>
                <div>
                    <h1 className="text-3xl font-bold text-surface-900 tracking-tight">System Settings</h1>
                    <p className="mt-1 text-surface-500">Configure global application parameters.</p>
                </div>
            </div>

            <div className="space-y-6">
                {/* General Settings */}
                <div className="glass-panel p-6 rounded-2xl">
                    <h2 className="text-lg font-semibold text-surface-900 mb-4 flex items-center gap-2">
                        <Shield className="text-primary-600" size={20} /> General Configuration
                    </h2>
                    <div className="space-y-4">
                        <div>
                            <label className="block text-sm font-medium text-surface-700 mb-1">System Name</label>
                            <input
                                type="text"
                                name="systemName"
                                value={config.systemName}
                                onChange={handleChange}
                                className="w-full px-4 py-2 bg-white border border-surface-200 rounded-lg focus:ring-2 focus:ring-primary-500 outline-none"
                            />
                        </div>
                        <div className="flex items-center gap-3">
                            <input
                                type="checkbox"
                                name="maintenanceMode"
                                id="maintenanceMode"
                                checked={config.maintenanceMode}
                                onChange={handleChange}
                                className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-surface-300 rounded"
                            />
                            <label htmlFor="maintenanceMode" className="text-sm font-medium text-surface-700">Maintenance Mode (Disable Student Access)</label>
                        </div>
                    </div>
                </div>

                {/* AI Configuration */}
                <div className="glass-panel p-6 rounded-2xl">
                    <h2 className="text-lg font-semibold text-surface-900 mb-4 flex items-center gap-2">
                        <Database className="text-emerald-600" size={20} /> AI Parameters
                    </h2>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div>
                            <label className="block text-sm font-medium text-surface-700 mb-1">Max Tokens</label>
                            <input
                                type="number"
                                name="maxTokens"
                                value={config.maxTokens}
                                onChange={handleChange}
                                className="w-full px-4 py-2 bg-white border border-surface-200 rounded-lg focus:ring-2 focus:ring-primary-500 outline-none"
                            />
                        </div>
                        <div>
                            <label className="block text-sm font-medium text-surface-700 mb-1">Log Level</label>
                            <select
                                name="logLevel"
                                value={config.logLevel}
                                onChange={handleChange}
                                className="w-full px-4 py-2 bg-white border border-surface-200 rounded-lg focus:ring-2 focus:ring-primary-500 outline-none"
                            >
                                <option>Debug</option>
                                <option>Info</option>
                                <option>Warning</option>
                                <option>Error</option>
                            </select>
                        </div>
                    </div>
                </div>

                <div className="flex justify-end">
                    <button className="btn-primary px-6 py-2 flex items-center gap-2">
                        <Save size={18} /> Save Changes
                    </button>
                </div>
            </div>
        </div>
    );
};

export default Settings;
