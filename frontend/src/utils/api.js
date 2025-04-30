import axios from 'axios';

const BASE_URL = 'http://127.0.0.1:8000/api';

const api = axios.create(
    {
        baseURL: BASE_URL,
    }
);

api.interceptors.request.use((config) =>
{
    const token = localStorage.getItem('token');
    if (token)
        config.headers.Authorization = `Bearer ${token}`;
    return config;
});

api.interceptors.response.use(
    (response) => response,
    (error) =>
    {
        if (error.response?.status === 401)
        {
            localStorage.removeItem('token');
            window.location.href = '/login';
        }
        return Promise.reject(error);
    }
);

export default api;
