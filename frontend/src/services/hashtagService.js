import api from "../utils/api";

export const getAllHashtags = async () =>
{
    const response = await api.get("/hashtags/all");
    return response.data;
};
