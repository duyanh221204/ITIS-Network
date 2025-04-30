import api from '../utils/api';
import qs from 'qs';

export const login = async (username, password) =>
{
    const response = await api.post('/auth/login',
        qs.stringify({ username, password }),
        {
            headers: 
                {
                    'Content-Type': 'application/x-www-form-urlencoded',
                }
        }
    );
    return response.data;
};

export const register = async (userData) =>
{
    const response = await api.post('/auth/register', userData);
    return response.data;
};

export const uploadImage = async (file) =>
{
    const formData = new FormData();
    formData.append('data', file);
    const response = await api.post('/images/upload', formData,
        {
            headers:
                {
                    'Content-Type': 'multipart/form-data',
                },
        }
    );
    return response.data;
};
