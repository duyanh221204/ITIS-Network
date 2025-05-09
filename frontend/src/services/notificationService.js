import api from "../utils/api";

export const getAllNotifications = async () =>
{
    const response = await api.get("/notifications/all");
    return response.data;
};

export const markNotificationAsRead = async (notificationId) =>
{
    const response = await api.put(`/notifications/${notificationId}`);
    return response.data;
};

export const getNotificationWsUrl = () =>
{
    const token = localStorage.getItem("token");
    return `ws://127.0.0.1:8000/api/notifications/ws?token=${token}`;
};
