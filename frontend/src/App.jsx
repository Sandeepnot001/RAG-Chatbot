import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Footer from './components/Footer';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import StudentChat from './pages/StudentChat';
import AdminDashboard from './pages/AdminDashboard';
import Logs from './pages/Logs';
import Settings from './pages/Settings';

import StudentLogin from './pages/StudentLogin';
import AdminLogin from './pages/AdminLogin';
import ProtectedRoute from './components/ProtectedRoute';

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-50 flex flex-col">
        <Navbar />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login/student" element={<StudentLogin />} />
          <Route path="/login/admin" element={<AdminLogin />} />

          <Route element={<ProtectedRoute role="student" />}>
            <Route path="/chat" element={<StudentChat />} />
          </Route>

          <Route element={<ProtectedRoute role="admin" />}>
            <Route path="/admin" element={<AdminDashboard />} />
            <Route path="/admin/logs" element={<Logs />} />
            <Route path="/admin/settings" element={<Settings />} />
          </Route>
        </Routes>
        <Footer />
      </div>
    </Router>
  );
}

export default App;
