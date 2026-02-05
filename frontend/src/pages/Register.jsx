import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { UserPlus, Shield, User, GraduationCap, AlertCircle, CheckCircle } from 'lucide-react';
import { API_BASE_URL } from '../apiConfig';

const Register = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [role, setRole] = useState('student');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [success, setSuccess] = useState(false);
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setLoading(true);

        try {
            const response = await fetch(`${API_BASE_URL}/auth/register`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ username, password, role }),
            });

            const contentType = response.headers.get("content-type");
            let data = {};
            if (contentType && contentType.indexOf("application/json") !== -1) {
                data = await response.json();
            } else {
                const text = await response.text();
                console.error("Invalid response:", text);
                throw new Error("Server error: Received HTML instead of JSON. Check if the backend is running and the API URL is correct.");
            }

            if (!response.ok) {
                throw new Error(data.detail || 'Registration failed');
            }

            setSuccess(true);
            setTimeout(() => {
                navigate(role === 'admin' ? '/login/admin' : '/login/student');
            }, 2000);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="flex min-h-screen items-center justify-center bg-gray-50 px-4 py-12 sm:px-6 lg:px-8">
            <div className="w-full max-w-md space-y-8 bg-white p-10 rounded-2xl shadow-xl">
                <div>
                    <div className="flex justify-center">
                        <div className="rounded-full bg-indigo-100 p-3">
                            <UserPlus className="h-10 w-10 text-indigo-600" />
                        </div>
                    </div>
                    <h2 className="mt-6 text-center text-3xl font-bold tracking-tight text-gray-900">
                        Create your account
                    </h2>
                    <p className="mt-2 text-center text-sm text-gray-600">
                        Join the CollegeBot platform
                    </p>
                </div>

                {error && (
                    <div className="rounded-md bg-red-50 p-4 flex items-center gap-3 text-red-700 text-sm">
                        <AlertCircle className="h-5 w-5" />
                        {error}
                    </div>
                )}

                {success && (
                    <div className="rounded-md bg-green-50 p-4 flex items-center gap-3 text-green-700 text-sm font-medium animate-pulse">
                        <CheckCircle className="h-5 w-5" />
                        Registration successful! Redirecting to login...
                    </div>
                )}

                <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
                    <div className="space-y-4 rounded-md shadow-sm">
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-1">Role</label>
                            <div className="grid grid-cols-2 gap-4">
                                <button
                                    type="button"
                                    onClick={() => setRole('student')}
                                    className={`flex items-center justify-center gap-2 p-3 rounded-lg border-2 transition-all ${role === 'student'
                                        ? 'border-indigo-600 bg-indigo-50 text-indigo-700'
                                        : 'border-gray-200 hover:border-gray-300 text-gray-500'
                                        }`}
                                >
                                    <GraduationCap className="h-5 w-5" />
                                    <span>Student</span>
                                </button>
                                <button
                                    type="button"
                                    onClick={() => setRole('admin')}
                                    className={`flex items-center justify-center gap-2 p-3 rounded-lg border-2 transition-all ${role === 'admin'
                                        ? 'border-indigo-600 bg-indigo-50 text-indigo-700'
                                        : 'border-gray-200 hover:border-gray-300 text-gray-500'
                                        }`}
                                >
                                    <Shield className="h-5 w-5" />
                                    <span>Admin</span>
                                </button>
                            </div>
                        </div>

                        <div>
                            <label htmlFor="username" className="block text-sm font-medium text-gray-700 mb-1">
                                Username (Email)
                            </label>
                            <div className="relative">
                                <span className="absolute inset-y-0 left-0 flex items-center pl-3">
                                    <User className="h-5 w-5 text-gray-400" />
                                </span>
                                <input
                                    id="username"
                                    name="username"
                                    type="text"
                                    required
                                    className="block w-full rounded-lg border-gray-300 pl-10 text-gray-900 focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm h-11"
                                    placeholder="Enter your username"
                                    value={username}
                                    onChange={(e) => setUsername(e.target.value)}
                                />
                            </div>
                        </div>
                        <div>
                            <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-1">
                                Password
                            </label>
                            <input
                                id="password"
                                name="password"
                                type="password"
                                required
                                className="block w-full rounded-lg border-gray-300 text-gray-900 focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm h-11"
                                placeholder="••••••••"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                            />
                        </div>
                    </div>

                    <div>
                        <button
                            type="submit"
                            disabled={loading || success}
                            className="group relative flex w-full justify-center rounded-lg bg-indigo-600 px-3 py-3 text-sm font-semibold text-white hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600 disabled:opacity-50 transition-all duration-200 shadow-lg shadow-indigo-200"
                        >
                            {loading ? 'Creating account...' : 'Create Account'}
                        </button>
                    </div>

                    <div className="text-center text-sm">
                        <span className="text-gray-600">Already have an account? </span>
                        <Link to={role === 'admin' ? '/login/admin' : '/login/student'} className="font-medium text-indigo-600 hover:text-indigo-500">
                            Log in here
                        </Link>
                    </div>
                </form>
            </div>
        </div>
    );
};

export default Register;
