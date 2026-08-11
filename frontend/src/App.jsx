import Settings from "./pages/Settings";
import React from "react";
import { Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import Footer from "./components/Footer";
import ChatbotWidget from "./components/ChatbotWidget";
import ProtectedRoute from "./components/ProtectedRoute";
import Home from "./pages/Home";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Destinations from "./pages/Destinations";
import DestinationDetail from "./pages/DestinationDetail";
import PlanTrip from "./pages/PlanTrip";
import TripPlanResult from "./pages/TripPlanResult";
import Dashboard from "./pages/Dashboard";
import Favorites from "./pages/Favorites";
import AdminDashboard from "./pages/AdminDashboard";

export default function App() {
  return (
    <div className="flex flex-col min-h-screen">
      <Navbar />
      <main className="flex-1">
        <Routes>
          <Route path="/settings" element={<ProtectedRoute><Settings /></ProtectedRoute>} />
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/destinations" element={<Destinations />} />
          <Route path="/destinations/:id" element={<DestinationDetail />} />

          <Route path="/plan" element={<ProtectedRoute><PlanTrip /></ProtectedRoute>} />
          <Route path="/trips/:id" element={<ProtectedRoute><TripPlanResult /></ProtectedRoute>} />
          <Route path="/dashboard" element={<ProtectedRoute><Dashboard /></ProtectedRoute>} />
          <Route path="/favorites" element={<ProtectedRoute><Favorites /></ProtectedRoute>} />
          <Route path="/admin" element={<ProtectedRoute adminOnly><AdminDashboard /></ProtectedRoute>} />

          <Route path="*" element={<div className="text-center py-24 text-ink-500">404 — Page not found</div>} />
        </Routes>
      </main>
      <Footer />
      <ChatbotWidget />
    </div>
  );
}