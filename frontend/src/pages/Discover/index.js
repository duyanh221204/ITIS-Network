import { useState, useEffect } from "react";
import { getNotFollowedUsers, followUser } from "../../services/profileService";
import { getAllHashtags } from "../../services/hashtagService";
import { getAllPosts } from "../../services/postService";
import UserList from "../../components/UserList";
import Post from "../../components/Post";
import "./styles.css";

const Discover = () =>
{
    const [users, setUsers] = useState([]);
    const [filteredUsers, setFilteredUsers] = useState([]);
    const [loading, setLoading] = useState(true);
    const [searchTerm, setSearchTerm] = useState("");
    const [error, setError] = useState("");
    const [tab, setTab] = useState("suggest-follow");
    const [hashtags, setHashtags] = useState([]);
    const [filteredHashtags, setFilteredHashtags] = useState([]);
    const [hashtagSearch, setHashtagSearch] = useState("");
    const [selectedHashtag, setSelectedHashtag] = useState(null);
    const [hashtagPosts, setHashtagPosts] = useState([]);
    const [loadingPosts, setLoadingPosts] = useState(false);

    useEffect(() =>
    {
        fetchUsers();
    }, []);

    useEffect(() =>
    {
        if (searchTerm.trim())
        {
            const filtered = users.filter(user =>
                user.username.toLowerCase().includes(searchTerm.toLowerCase())
            );
            setFilteredUsers(filtered);
        }
        else
            setFilteredUsers(users);
    }, [searchTerm, users]);

    useEffect(() =>
    {
        if (tab === "discover-hashtag")
            fetchHashtags();
    }, [tab]);

    const fetchUsers = async () =>
    {
        setLoading(true);
        try
        {
            const response = await getNotFollowedUsers();
            if (response.status === "ok")
            {
                setUsers(response.data || []);
                setFilteredUsers(response.data || []);
            }
            else
                setError("Failed to fetch users");
        }
        catch (error)
        {
            setError("Error loading users");
            throw error;
        }
        finally
        {
            setLoading(false);
        }
    };

    const fetchHashtags = async () =>
    {
        const res = await getAllHashtags();
        if (res.status === "ok" && Array.isArray(res.data))
        {
            setHashtags(res.data);
            setFilteredHashtags(res.data);
        }
    };

    useEffect(() =>
    {
        if (tab === "discover-hashtag")
        {
            if (hashtagSearch.trim())
            {
                setFilteredHashtags(
                    hashtags.filter(h => h.name.toLowerCase().includes(hashtagSearch.toLowerCase()))
                );
            }
            else
            {
                setFilteredHashtags(hashtags);
            }
        }
    }, [hashtagSearch, hashtags, tab]);

    const handleSelectHashtag = async (name) =>
    {
        setSelectedHashtag(name);
        setLoadingPosts(true);
        const res = await getAllPosts();
        if (res.status === "ok" && Array.isArray(res.data))
        {
            const filtered = res.data.filter(post =>
                Array.isArray(post.hashtags) && post.hashtags.some(h => h.name.toLowerCase() === name.toLowerCase())
            );
            setHashtagPosts(filtered);
        }
        else
        {
            setHashtagPosts([]);
        }
        setLoadingPosts(false);
    };

    return (
        <div className="discover-page">
            <h1 className="page-title">Discover</h1>
            <div className="discover-tabs">
                <button className={tab === "suggest-follow" ? "active" : ""} onClick={() => setTab("suggest-follow")}>Suggest Follow</button>
                <button className={tab === "discover-hashtag" ? "active" : ""} onClick={() => setTab("discover-hashtag")}>Discover Hashtag</button>
            </div>
            <div className="search-container">
                {
                    tab === "suggest-follow" ?
                        (
                            <input
                                className="search-input"
                                type="text"
                                placeholder="Search people..."
                                value={searchTerm}
                                onChange={e => setSearchTerm(e.target.value)}
                            />
                        ) :
                        (
                            <input
                                className="search-input"
                                type="text"
                                placeholder="Search hashtag..."
                                value={hashtagSearch}
                                onChange={e => setHashtagSearch(e.target.value)}
                            />
                        )
                }
            </div>
            {
                tab === "suggest-follow" ?
                    (
                        <div className="users-container">
                            {
                                loading ?
                                    (
                                        <div className="loading"><div className="loading-spinner"></div></div>
                                    ) :
                                    error ?
                                        (
                                            <div className="error-container">{error}</div>
                                        ) :
                                        (
                                            <UserList users={filteredUsers} title={null} emptyMessage="No users found" onFollowAction={async (id) =>
                                            {
                                                await followUser(id);
                                                fetchUsers();
                                            }} />
                                        )
                            }
                        </div>
                    ) : (
                        <div className="hashtags-container">
                            {
                                filteredHashtags.length === 0 ?
                                    (
                                        <div className="empty-message">No hashtags found</div>
                                    ) :
                                    (
                                        <ul className="hashtag-list-discover">
                                            {
                                                filteredHashtags.map(h => (
                                                    <li
                                                        key={h.id}
                                                        className={`hashtag-item-discover${selectedHashtag === h.name ? " selected" : ""}`}
                                                        onClick={() => handleSelectHashtag(h.name)}
                                                    >
                                                        #{h.name}
                                                    </li>
                                                ))
                                            }
                                        </ul>
                                    )
                            }
                            {
                                selectedHashtag &&
                                (
                                    <div className="hashtag-posts-container">
                                        <h2 className="hashtag-posts-title">Posts with <span className="hashtag-highlight">#{selectedHashtag}</span></h2>
                                        {
                                            loadingPosts ?
                                                (
                                                    <div className="loading"><div className="loading-spinner"></div></div>
                                                ) :
                                                hashtagPosts.length === 0 ?
                                                    (
                                                        <div className="empty-message">No posts found for this hashtag.</div>
                                                    ) :
                                                    (
                                                        hashtagPosts.map(post => <Post key={post.id} post={post} refreshPosts={null} />)
                                                    )
                                        }
                                    </div>
                                )
                            }
                        </div>
                    )
            }
        </div>
    );
}

export default Discover;
