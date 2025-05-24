import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { getUserProfile, updateUserInfo, updatePassword } from "../../services/profileService";
import { uploadImage } from "../../services/authService";
import "./styles.css";

const Settings = ({page}) =>
{
    const navigate = useNavigate();
    const [profileData, setProfileData] = useState(
        {
            username: "",
            email: "",
            introduction: "",
            avatar: null
        }
    );
    const [passwordData, setPasswordData] = useState(
        {
            current_password: "",
            new_password: "",
            confirm_password: ""
        }
    );
    const [currentAvatar, setCurrentAvatar] = useState("");
    const [previewUrl, setPreviewUrl] = useState("");
    const [loading, setLoading] = useState(true);
    const [saveLoading, setSaveLoading] = useState(false);
    const [passwordLoading, setPasswordLoading] = useState(false);
    const [profileError, setProfileError] = useState("");
    const [passwordError, setPasswordError] = useState("");
    const [profileSuccess, setProfileSuccess] = useState("");
    const [passwordSuccess, setPasswordSuccess] = useState("");
    const currentUserId = localStorage.getItem("userId");

    useEffect(() =>
    {
        fetchProfileData();
    }, []);

    const fetchProfileData = async () =>
    {
        setLoading(true);
        try
        {
            const response = await getUserProfile(currentUserId);
            if (response.status === "ok" && response.data)
            {
                const {username, email, introduction, avatar} = response.data;
                setProfileData({username, email, introduction});
                setCurrentAvatar(avatar);
            }
        }
        catch (error)
        {
            throw error;
        }
        finally
        {
            setLoading(false);
        }
    };

    const handleProfileChange = (e) =>
    {
        const {name, value} = e.target;
        setProfileData
            (
                {
                    ...profileData,
                    [name]: value
                }
            );
    };

    const handleFileChange = (e) =>
    {
        if (e.target.files && e.target.files[0])
        {
            const file = e.target.files[0];
            const reader = new FileReader();
            reader.onload = (e) =>
            {
                setPreviewUrl(e.target.result);
            };
            reader.readAsDataURL(file);
            setProfileData
                (
                    {
                        ...profileData,
                        avatar: file
                    }
                );
        }
    };

    const handlePasswordChange = (e) =>
    {
        const {name, value} = e.target;
        setPasswordData
            (
                {
                    ...passwordData,
                    [name]: value
                }
            );
    };

    const handleUpdateProfile = async (e) =>
    {
        e.preventDefault();
        setProfileError("");
        setProfileSuccess("");
        setSaveLoading(true);

        try
        {
            let avatarUrl = currentAvatar;
            if (profileData.avatar)
            {
                const imageResponse = await uploadImage(profileData.avatar);
                avatarUrl = imageResponse.data;
            }

            const updateData = {
                username: profileData.username,
                introduction: profileData.introduction,
                avatar: avatarUrl
            };
            const response = await updateUserInfo(updateData);

            if (response.status === "ok")
            {
                setProfileSuccess("Profile updated successfully");
                setCurrentAvatar(avatarUrl);
            }
            else
                setProfileError("Failed to update profile");
        }
        catch (error)
        {
            setProfileError(error.response?.data?.message || "Error updating profile");
        }
        finally
        {
            setSaveLoading(false);
        }
    };

    const handleUpdatePassword = async (e) =>
    {
        e.preventDefault();
        setPasswordError("");
        setPasswordSuccess("");

        if (passwordData.new_password !== passwordData.confirm_password)
        {
            setPasswordError("Passwords don't match");
            return;
        }

        setPasswordLoading(true);
        try
        {
            const response = await updatePassword
                (
                    {
                        current_password: passwordData.current_password,
                        new_password: passwordData.new_password
                    }
                );

            if (response.status === "ok")
            {
                setPasswordSuccess("Password updated successfully");
                setPasswordData(
                    {
                        current_password: "",
                        new_password: "",
                        confirm_password: ""
                    }
                );
            }
            else
                setPasswordError("Failed to update password");
        }
        catch (error)
        {
            setPasswordError(error.response?.data?.message || "Error updating password");
        }
        finally
        {
            setPasswordLoading(false);
        }
    };

    return (
        <div className="settings-page">
            <h1 className="page-title">Account Settings</h1>
            <div className="settings-nav">
                <button className={page === "profile-info" ? "active" : ""} onClick={() => navigate("/settings/profile-info")}>Profile Information</button>
                <button className={page === "change-password" ? "active" : ""} onClick={() => navigate("/settings/change-password")}>Change Password</button>
            </div>
            {
                loading ?
                    (
                        <div className="loading">
                            <div className="loading-spinner"></div>
                        </div>
                    ) :
                    (
                        <div className="settings-container">
                            {
                                page === 'profile-info' &&
                                (
                                    <div className="settings-section">
                                        <h2 className="section-title">Profile Information</h2>
                                        <form onSubmit={handleUpdateProfile}>
                                            <div className="form-group">
                                                <label htmlFor="username">Username</label>
                                                <input
                                                    type="text"
                                                    id="username"
                                                    name="username"
                                                    className="input-field"
                                                    value={profileData.username}
                                                    onChange={handleProfileChange}
                                                    required
                                                />
                                            </div>
                                            <div className="form-group">
                                                <label htmlFor="email">Email</label>
                                                <input
                                                    type="email"
                                                    id="email"
                                                    name="email"
                                                    className="input-field"
                                                    value={profileData.email}
                                                    disabled
                                                    required
                                                />
                                            </div>
                                            <div className="form-group">
                                                <label htmlFor="introduction">Introduction</label>
                                                <textarea
                                                    id="introduction"
                                                    name="introduction"
                                                    className="input-field"
                                                    value={profileData.introduction || ""}
                                                    onChange={handleProfileChange}
                                                ></textarea>
                                            </div>
                                            <div className="form-group">
                                                <label>Profile Photo</label>
                                                <div className="avatar-container">
                                                    <img
                                                        src={previewUrl || currentAvatar || "/default_avatar.png"}
                                                        alt="Profile avatar"
                                                        className="avatar-preview"
                                                    />
                                                    <div className="avatar-upload">
                                                        <label htmlFor="avatar" className="file-input-label">
                                                            Change Profile Photo
                                                            <input
                                                                type="file"
                                                                id="avatar"
                                                                name="avatar"
                                                                className="file-input"
                                                                accept="image/*"
                                                                onChange={handleFileChange}
                                                            />
                                                        </label>
                                                    </div>
                                                </div>
                                            </div>
                                            {
                                                profileError && <div className="error-message">{profileError}</div>
                                            }
                                            {
                                                profileSuccess && <div className="success-message">{profileSuccess}</div>
                                            }
                                            <button
                                                type="submit"
                                                className="btn btn-primary"
                                                disabled={saveLoading}
                                            >
                                                {
                                                    saveLoading ? <div className="loading-spinner"></div> : "Save Changes"
                                                }
                                            </button>
                                        </form>
                                    </div>
                                )
                            }
                            {
                                page === "change-password" &&
                                (
                                    <div className="settings-section">
                                        <h2 className="section-title">Change Password</h2>
                                        <form onSubmit={handleUpdatePassword}>
                                            <div className="form-group">
                                                <label htmlFor="current_password">Current Password</label>
                                                <input
                                                    type="password"
                                                    id="current_password"
                                                    name="current_password"
                                                    className="input-field"
                                                    value={passwordData.current_password}
                                                    onChange={handlePasswordChange}
                                                    required
                                                />
                                            </div>
                                            <div className="form-group">
                                                <label htmlFor="new_password">New Password</label>
                                                <input
                                                    type="password"
                                                    id="new_password"
                                                    name="new_password"
                                                    className="input-field"
                                                    value={passwordData.new_password}
                                                    onChange={handlePasswordChange}
                                                    required
                                                />
                                            </div>
                                            <div className="form-group">
                                                <label htmlFor="confirm_password">Confirm New Password</label>
                                                <input
                                                    type="password"
                                                    id="confirm_password"
                                                    name="confirm_password"
                                                    className="input-field"
                                                    value={passwordData.confirm_password}
                                                    onChange={handlePasswordChange}
                                                    required
                                                />
                                            </div>
                                            {
                                                passwordError && <div className="error-message">{passwordError}</div>
                                            }
                                            {
                                                passwordSuccess && <div className="success-message">{passwordSuccess}</div>
                                            }
                                            <button
                                                type="submit"
                                                className="btn btn-primary"
                                                disabled={passwordLoading}
                                            >
                                                {
                                                    passwordLoading ? <div className="loading-spinner"></div> : "Update Password"
                                                }
                                            </button>
                                        </form>
                                    </div>
                                )
                            }
                        </div>
                    )
            }
        </div>
    );
}

export default Settings;
