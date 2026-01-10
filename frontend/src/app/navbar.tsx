'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { getCurrentUser, logout } from '@/lib/api';

export default function Navbar() {
  const [isLoggedIn, setIsLoggedIn] = useState<boolean | null>(null); // null means loading
  const [user, setUser] = useState<any>(null);
  const router = useRouter();

  useEffect(() => {
    // Check if user is logged in by trying to get user info
    const checkAuth = async () => {
      try {
        const userData = await getCurrentUser();
        setUser(userData);
        setIsLoggedIn(true);
      } catch (error) {
        setIsLoggedIn(false);
      }
    };

    checkAuth();
  }, []);

  const handleLogout = async () => {
    try {
      await logout();
      setIsLoggedIn(false);
      setUser(null);
      router.push('/login');
      router.refresh();
    } catch (error) {
      console.error('Logout error:', error);
      // Even if API logout fails, clear local token
      localStorage.removeItem('auth_token');
      setIsLoggedIn(false);
      setUser(null);
      router.push('/login');
    }
  };

  return (
    <nav className="bg-primary-600 text-white shadow-md">
      <div className="container mx-auto px-4 py-4 flex justify-between items-center">
        <h1 className="text-2xl font-bold">Todo App</h1>
        <div className="flex items-center space-x-4">
          {isLoggedIn === null ? (
            // Loading state
            <div className="h-6 w-20 bg-primary-400 rounded animate-pulse"></div>
          ) : isLoggedIn ? (
            // Logged in state
            <>
              <span className="hidden md:inline">Welcome, {user?.full_name || user?.email}</span>
              <button 
                onClick={handleLogout}
                className="px-4 py-2 bg-primary-700 text-white rounded-md hover:bg-primary-800 transition-colors text-sm"
              >
                Logout
              </button>
            </>
          ) : (
            // Not logged in state
            <>
              <a 
                href="/login" 
                className="px-4 py-2 bg-primary-700 text-white rounded-md hover:bg-primary-800 transition-colors text-sm"
              >
                Login
              </a>
              <a 
                href="/register" 
                className="px-4 py-2 bg-white text-primary-600 rounded-md hover:bg-gray-100 transition-colors text-sm"
              >
                Register
              </a>
            </>
          )}
        </div>
      </div>
    </nav>
  );
}