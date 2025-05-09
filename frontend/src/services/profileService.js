import api from "../utils/api";

export const getUserProfile = async (userId) =>
{
    const response = await api.get(`/profile/${userId}`);
    return response.data;
};

export const updateUserInfo = async (userData) =>
{
    const response = await api.put("/profile/update-info", userData);
    return response.data;
};

export const updatePassword = async (passwordData) =>
{
    const response = await api.put("/users/update-password", passwordData);
    return response.data;
};

export const followUser = async (userId) =>
{
    const response = await api.post(`/users/follow/${userId}`);
    return response.data;
};

export const unfollowUser = async (userId) =>
{
    const response = await api.delete(`/users/unfollow/${userId}`);
    return response.data;
};

export const getNotFollowedUsers = async () =>
{
    const response = await api.get("/users");
    return response.data;
};
