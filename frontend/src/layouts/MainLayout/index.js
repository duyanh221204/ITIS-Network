import { useEffect } from "react";
import { Routes, Route, Navigate } from "react-router-dom";
import Header from "../../components/Header";
import Sidebar from "../../components/Sidebar";
import Home from "../../pages/Home";
import FollowingPosts from "../../pages/FollowingPosts";
import CreatePost from "../../pages/CreatePost";
import Profile from "../../pages/Profile";
import Settings from "../../pages/Settings";
import Discover from "../../pages/Discover";
import Chat from "../../pages/Chat";
import "./styles.css";

const MainLayout = () =>
{
    useEffect(() =>
    {
        try
        {
            const token = localStorage.getItem("token");
            if (token)
            {
                const base64Url = token.split(".")[1];
                const base64 = base64Url.replace(/-/g, "+").replace(/_/g, "/");
                const jsonPayload = decodeURIComponent
                (
                    window.atob(base64).split("").map(c =>
                    {
                        return "%" + ("00" + c.charCodeAt(0).toString(16)).slice(-2);
                    }).join("")
                );

                const {id} = JSON.parse(jsonPayload);
                if (id)
                    localStorage.setItem("userId", id);
            }
        }
        catch (error)
        {
            throw error;
        }
    }, []);

    return (
        <div className="main-layout">
            <Header />
            <div className="content-wrapper">
                <Sidebar />
                <main className="main-content">
                    <Routes>
                        <Route path="/" element={<Home />} />
                        <Route path="/following-posts" element={<FollowingPosts />} />
                        <Route path="/create-post" element={<CreatePost />} />
                        <Route path="/profile/:userId" element={<Profile />} />
                        <Route path="/settings" element={<Navigate to="/settings/profile-info" replace />} />
                        <Route path="/settings/profile-info" element={<Settings page="profile-info" />} />
                        <Route path="/settings/change-password" element={<Settings page="change-password" />} />
                        <Route path="/discover" element={<Discover />} />
                        <Route path="/chat" element={<Chat />} />
                        <Route path="/chat/:conversationId" element={<Chat />} />
                        <Route path="*" element={<Navigate to="/" />} />
                    </Routes>
                </main>
            </div>
        </div>
    );
}

export default MainLayout;
