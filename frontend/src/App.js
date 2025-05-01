import { BrowserRouter, Route, Routes, Navigate } from 'react-router-dom';
import { useState, useEffect } from 'react';
import Login from './pages/Auth/Login';
import Register from './pages/Auth/Register';
import MainLayout from './layouts/MainLayout';
import './styles/global.css';

const App = () =>
{
  const [isAuthenticated, setIsAuthenticated] = useState(!!localStorage.getItem('token'));

  useEffect(() =>
  {
    const handleStorage = () =>
    {
      setIsAuthenticated(!!localStorage.getItem('token'));
    };
    window.addEventListener('storage', handleStorage);
    return () => window.removeEventListener('storage', handleStorage);
  }, []);

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={ !isAuthenticated ? <Login setIsAuthenticated={ setIsAuthenticated } /> : <Navigate to={ window.location.pathname !== '/login' ? window.location.pathname : window.location.pathname } /> } />
        <Route path="/register" element={ !isAuthenticated ? <Register /> : <Navigate to={ window.location.pathname !== '/register' ? window.location.pathname : window.location.pathname } /> } />
        <Route path="/*" element={ isAuthenticated ? <MainLayout /> : <Navigate to="/login" /> } />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
