import api from "../utils/api";

export const getOrCreateConversation = async (userId) =>
{
    const response = await api.post("/chats/conversation", { user_id: userId });
    return response.data;
};

export const getAllConversations = async () =>
{
    const response = await api.get("/chats/conversations");
    return response.data;
};

export const getAllMessages = async (conversationId) =>
{
    const response = await api.get(`/chats/conversation/${conversationId}/messages`);
    return response.data;
};

export const sendMessage = async (conversationId, content) =>
{
    const response = await api.post(`/chats/conversations/${conversationId}/message`, {content});
    return response.data;
};

export const markConversationAsRead = async (conversationId) =>
{
    const response = await api.put(`/chats/conversations/${conversationId}/read`);
    return response.data;
};

export const getUnreadConversations = async () =>
{
    const response = await api.get("/chats/conversations/unread");
    return response.data;
};

export const getWebSocketUrl = (conversationId) =>
{
    const token = localStorage.getItem("token");
    return `ws://127.0.0.1:8000/api/chats/ws/${conversationId}?token=${token}`;
};
