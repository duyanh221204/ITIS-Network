import { useState, useEffect } from "react";
import { getFollowingPosts } from "../../services/postService";
import Post from "../../components/Post";
import "./styles.css";

const FollowingPosts = () =>
{
    const [posts, setPosts] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    useEffect(() =>
    {
        fetchPosts();
    }, []);

    const fetchPosts = async () =>
    {
        setLoading(true);
        try
        {
            const response = await getFollowingPosts();
            if (response.status === "ok")
                setPosts(response.data || []);
            else
                setError("Failed to fetch posts");
        }
        catch (error)
        {
            setError("Error loading posts");
        }
        finally
        {
            setLoading(false);
        }
    };

    return (
        <div className="following-posts-page">
            <h1 className="page-title">Following Posts</h1>
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
                                <button onClick={fetchPosts} className="btn btn-primary">
                                    Try Again
                                </button>
                            </div>
                        ) :
                        posts.length > 0 ?
                            (
                                <div className="posts-container">
                                    {
                                        posts.map(post => (
                                            <Post key={post.id} post={post} refreshPosts={fetchPosts} />
                                        ))
                                    }
                                </div>
                            ) : (
                                <div className="empty-posts">
                                    <p>No posts yet.</p>
                                </div>
                            )
            }
        </div>
    );
}

export default FollowingPosts;
