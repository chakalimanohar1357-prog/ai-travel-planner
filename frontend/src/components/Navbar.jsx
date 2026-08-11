import ThemeToggle from "./ThemeToggle";
import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { Plane, Menu, X, User } from "lucide-react";
import { useAuth } from "../context/AuthContext";

export default function Navbar() {
  const { user, logout } = useAuth();
  const [open, setOpen] = useState(false);
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/");
  };

  const links = [
    { to: "/destinations", label: "Explore" },
    { to: "/plan", label: "Plan a Trip" },
    { to: "/dashboard", label: "My Trips" },
    { to: "/favorites", label: "Favorites" },
  ];

  return (
    <header className="sticky top-0 z-40 bg-white/90 backdrop-blur border-b border-gray-100 dark:bg-gray-900/90 dark:border-gray-800">
      <nav className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        <Link to="/" className="flex items-center gap-2.5 group">
          <span className="relative flex items-center justify-center w-9 h-9 rounded-xl bg-gradient-to-br from-primary-400 via-primary-500 to-primary-700 shadow-md group-hover:scale-105 transition-transform">
            <Plane size={17} className="text-white -rotate-45" strokeWidth={2.5} />
            <span className="absolute -bottom-0.5 -right-0.5 w-2.5 h-2.5 rounded-full bg-primary-100 border-2 border-white" />
          </span>
          <span className="font-display font-bold text-xl tracking-tight text-ink-900 dark:text-white">
            Travel<span className="text-primary-500">AI</span>
          </span>
        </Link>

        <div className="hidden md:flex items-center gap-6">
          {links.map((l) => (
            <Link key={l.to} to={l.to} className="text-sm font-medium text-ink-700 hover:text-primary-600 transition-colors dark:text-gray-300 dark:hover:text-primary-400">
              {l.label}
            </Link>
          ))}
        </div>

        <div className="hidden md:flex items-center gap-3">
          <ThemeToggle />
          {user ? (
            <>
              {user.role === "admin" && (
                <Link to="/admin" className="text-sm font-medium text-ink-700 hover:text-primary-600 dark:text-gray-300 dark:hover:text-primary-400">
                  Admin
                </Link>
              )}
              <Link to="/settings" className="text-sm font-medium text-ink-700 hover:text-primary-600 dark:text-gray-300 dark:hover:text-primary-400">
                Settings
              </Link>
              <div className="flex items-center gap-2 text-sm font-medium text-ink-700 dark:text-gray-300">
                <User size={16} /> {user.name}
              </div>
              <button onClick={handleLogout} className="btn-outline text-sm py-2">
                Logout
              </button>
            </>
          ) : (
            <>
              <Link to="/login" className="text-sm font-medium text-ink-700 hover:text-primary-600 dark:text-gray-300 dark:hover:text-primary-400">
                Login
              </Link>
              <Link to="/register" className="btn-primary text-sm">
                Sign Up
              </Link>
            </>
          )}
        </div>

        <div className="md:hidden flex items-center gap-2">
          <ThemeToggle />
          <button onClick={() => setOpen(!open)}>
            {open ? <X className="dark:text-white" /> : <Menu className="dark:text-white" />}
          </button>
        </div>
      </nav>

      {open && (
        <div className="md:hidden px-4 pb-4 flex flex-col gap-3 bg-white border-t border-gray-100 dark:bg-gray-900 dark:border-gray-800">
          {links.map((l) => (
            <Link key={l.to} to={l.to} onClick={() => setOpen(false)} className="text-sm font-medium text-ink-700 dark:text-gray-300">
              {l.label}
            </Link>
          ))}
          {user ? (
            <>
              <Link to="/settings" onClick={() => setOpen(false)} className="text-sm font-medium text-ink-700 dark:text-gray-300">
                Settings
              </Link>
              <button onClick={handleLogout} className="btn-outline text-sm w-full">Logout</button>
            </>
          ) : (
            <>
              <Link to="/login" onClick={() => setOpen(false)} className="text-sm font-medium dark:text-gray-300">Login</Link>
              <Link to="/register" onClick={() => setOpen(false)} className="btn-primary text-sm text-center">Sign Up</Link>
            </>
          )}
        </div>
      )}
    </header>
  );
}