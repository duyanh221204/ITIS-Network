import api from '../utils/api';

export const getAllNotifications = async () =>
{
    const response = await api.get('/notifications/all');
    return response.data;
};

export const markNotificationAsRead = async (notificationId) =>
{
    const response = await api.put(`/notifications/${notificationId}`);
    return response.data;
};
