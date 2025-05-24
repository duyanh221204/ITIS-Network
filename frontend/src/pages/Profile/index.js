import { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { getUserProfile, followUser, unfollowUser } from "../../services/profileService";
import { getUserPosts } from "../../services/postService";
import { getOrCreateConversation } from "../../services/chatService";
import Post from "../../components/Post";
import UserList from "../../components/UserList";
import "./styles.css";

const Profile = () =>
{
    const {userId} = useParams();
    const navigate = useNavigate();
    const [profile, setProfile] = useState(null);
    const [posts, setPosts] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");
    const [showFollowers, setShowFollowers] = useState(false);
    const [showFollowing, setShowFollowing] = useState(false);
    const [isCurrentUser, setIsCurrentUser] = useState(false);
    const currentUserId = (localStorage.getItem("userId") || "").toString();

    useEffect(() =>
    {
        fetchProfileAndPosts();
        setShowFollowers(false);
        setShowFollowing(false);
    }, [userId]);

    const fetchProfileAndPosts = async () =>
    {
        setLoading(true);
        try
        {
            let profileId = userId;
            if (!profileId || profileId === "me")
                profileId = currentUserId;

            setIsCurrentUser(userId === "me" || userId === currentUserId);

            const profileResponse = await getUserProfile(profileId);
            if (profileResponse.status === "ok" && profileResponse.data)
            {
                setProfile(profileResponse.data);
                const postsResponse = await getUserPosts(profileResponse.data.id);

                if (postsResponse.status === "ok")
                    setPosts(postsResponse.data || []);
            }
            else
                setError("Failed to load profile");
        }
        catch (error)
        {
            setError("Error loading profile: " + (error.message || error));
            throw error;
        }
        finally
        {
            setLoading(false);
        }
    };

    const handleFollow = async () =>
    {
        if (!profile)
            return;

        if (window.confirm(`Are you sure you want to follow ${profile.username}?`))
        {
            try
            {
                await followUser(profile.id);
                fetchProfileAndPosts();
            }
            catch (error)
            {
                throw error;
            }
        }
    };

    const handleUnfollow = async () =>
    {
        if (!profile)
            return;

        if (window.confirm(`Are you sure you want to unfollow ${profile.username}?`))
        {
            try
            {
                await unfollowUser(profile.id);
                fetchProfileAndPosts();
            }
            catch (error)
            {
                throw error;
            }
        }
    };

    const handleMessage = async () =>
    {
        if (!profile)
            return;

        try
        {
            const response = await getOrCreateConversation(profile.id);
            if (response.status === "ok" && response.data)
                navigate(`/chat/${ response.data.id }`);
        }
        catch (error)
        {
            throw error;
        }
    };

    const checkIsFollowing = () =>
    {
        if (!profile || !currentUserId)
            return false;
        return profile.followers.some(follower => follower.id.toString() === currentUserId);
    };

    const checkIsFollower = () =>
    {
        if (!profile || !currentUserId)
            return false;
        return profile.followings.some(following => following.id.toString() === currentUserId);
    };

    return (
        <div className="profile-page">
            {
                loading ?
                    (
                        <div className="loading">
                            <div className="loading-spinner"></div>
                        </div>
                    ) :
                    error ?
                        (
                            <div className="error-container">
                                <p className="error-message">{error}</p>
                                <button onClick={fetchProfileAndPosts} className="btn btn-primary">
                                    Try Again
                                </button>
                            </div>
                        ) :
                        profile ?
                            (
                                <div className="profile-container">
                                    <div className="profile-header">
                                        <div className="profile-avatar-container">
                                            <img
                                                src={profile.avatar || "/default_avatar.png"}
                                                alt={profile.username}
                                                className="profile-avatar"
                                            />
                                        </div>

                                        <div className="profile-info">
                                            <h1 className="profile-username">{profile.username}</h1>
                                            <p className="profile-email">{profile.email}</p>

                                            {
                                                profile.introduction &&
                                                (
                                                    <p className="profile-introduction">{profile.introduction}</p>
                                                )
                                            }

                                            <div className="profile-stats">
                                                <div className="stat-item" onClick={() => setShowFollowers(true)}>
                                                    <span className="stat-number">{profile.followers.length}</span>
                                                    <span className="stat-label">Followers</span>
                                                </div>
                                                <div className="stat-item" onClick={() => setShowFollowing(true)}>
                                                    <span className="stat-number">{profile.followings.length}</span>
                                                    <span className="stat-label">Following</span>
                                                </div>
                                                <div className="stat-item">
                                                    <span className="stat-number">{posts.length}</span>
                                                    <span className="stat-label">Posts</span>
                                                </div>
                                            </div>

                                            {
                                                !isCurrentUser &&
                                                (
                                                    <div className="profile-actions">
                                                        {
                                                            checkIsFollowing() ?
                                                                (
                                                                    <button className="btn btn-secondary" onClick={handleUnfollow}>
                                                                        Unfollow
                                                                    </button>
                                                                ) :
                                                                (
                                                                    <button className="btn btn-primary" onClick={handleFollow}>
                                                                        {
                                                                            checkIsFollower() ? "Follow back" : "Follow"
                                                                        }
                                                                    </button>
                                                                )
                                                        }
                                                        <button className="btn btn-secondary" onClick={handleMessage}>
                                                            Message
                                                        </button>
                                                    </div>
                                                )
                                            }

                                            {
                                                isCurrentUser &&
                                                (
                                                    <div className="profile-actions">
                                                        <button
                                                            className="btn btn-primary"
                                                            onClick={() => navigate("/settings")}
                                                        >
                                                            Edit Profile
                                                        </button>
                                                    </div>
                                                )
                                            }
                                        </div>
                                    </div>

                                    <div className="profile-content">
                                        <h2 className="section-title">Posts</h2>
                                        {
                                            posts.length > 0 ?
                                                (
                                                    <div className="posts-container">
                                                        {
                                                            posts.map(post =>
                                                            (
                                                                <Post key={post.id} post={post} refreshPosts={fetchProfileAndPosts} />
                                                            ))
                                                        }
                                                    </div>
                                                ) :
                                                (
                                                    <div className="empty-posts">
                                                        <p>No posts yet.</p>
                                                    </div>
                                                )
                                        }
                                    </div>

                                    {
                                        showFollowers &&
                                        (
                                            <div className="modal-overlay">
                                                <div className="modal">
                                                    <div className="modal-header">
                                                        <h3>Followers</h3>
                                                        <button className="modal-close" onClick={() => setShowFollowers(false)}>×</button>
                                                    </div>
                                                    <div className="modal-body">
                                                        <UserList
                                                            users={profile.followers}
                                                            emptyMessage="No followers yet."
                                                        />
                                                    </div>
                                                </div>
                                            </div>
                                        )
                                    }

                                    {
                                        showFollowing &&
                                        (
                                            <div className="modal-overlay">
                                                <div className="modal">
                                                    <div className="modal-header">
                                                        <h3>Following</h3>
                                                        <button className="modal-close" onClick={() => setShowFollowing(false)}>×</button>
                                                    </div>
                                                    <div className="modal-body">
                                                        <UserList
                                                            users={profile.followings}
                                                            emptyMessage="Not following anyone yet."
                                                        />
                                                    </div>
                                                </div>
                                            </div>
                                        )
                                    }
                                </div>
                            ) :
                            null
            }
        </div>
    );
}

export default Profile;
