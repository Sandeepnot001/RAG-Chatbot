import React from 'react';
import { Navigate, Outlet } from 'react-router-dom';

const ProtectedRoute = ({ role }) => {
    const token = localStorage.getItem('token');
    const userRole = localStorage.getItem('role');

    if (!token) {
        if (role === 'admin') {
            return <Navigate to="/login/admin" replace />;
        } else {
            return <Navigate to="/login/student" replace />;
        }
    }

    if (role && userRole !== role) {
        return <Navigate to="/" replace />; // Unauthorized, redirect home
    }

    return <Outlet />;
};

export default ProtectedRoute;
