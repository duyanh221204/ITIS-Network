import {useState, useEffect} from "react";
import {getAllPosts} from "../../services/postService";
import Post from "../../components/Post";
import "./styles.css";

const Home = () =>
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
            const response = await getAllPosts();
            if (response.status === "ok")
                setPosts(response.data || []);
            else
                setError("Failed to fetch posts");
        }
        catch (error)
        {
            setError("Error loading posts");
            throw error;
        }
        finally
        {
            setLoading(false);
        }
    };

    return (
        <div className="home-page">
            <h1 className="page-title">News Feed</h1>

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
                        (
                            <>
                                {
                                    posts.length > 0 ?
                                        (
                                            <div className="posts-container">
                                                {
                                                    posts.map(post =>
                                                        (
                                                            <Post key={post.id} post={post} refreshPosts={fetchPosts} />
                                                        )
                                                    )
                                                }
                                            </div>
                                        ) :
                                        (
                                            <div className="empty-posts">
                                                <p>No posts yet. Create a post or follow other users to see their posts here!</p>
                                            </div>
                                        )
                                }
                            </>
                        )
            }
        </div>
    );
}

export default Home;
