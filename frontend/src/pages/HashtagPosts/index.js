import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import Post from "../../components/Post";
import { getAllPosts } from "../../services/postService";
import "../Home/styles.css";

const HashtagPosts = () =>
{
    const { hashtag } = useParams();
    const [posts, setPosts] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() =>
    {
        const fetchPosts = async () =>
        {
            setLoading(true);
            const res = await getAllPosts();
            if (res.status === "ok" && Array.isArray(res.data))
            {
                const filtered = res.data.filter(post =>
                    Array.isArray(post.hashtags) && post.hashtags.some(h => h.name.toLowerCase() === hashtag.toLowerCase())
                );
                setPosts(filtered);
            }
            setLoading(false);
        };
        fetchPosts();
    }, [hashtag]);

    return (
        <div className="news-feed-page">
            <h1 className="page-title"># { hashtag }</h1>
            <div className="news-feed-container" style={ { maxWidth: 600, margin: "32px auto" } }>
                { loading ? (
                    <div className="loading"><div className="loading-spinner"></div></div>
                ) : posts.length === 0 ? (
                    <div className="empty-message">No posts found for this hashtag.</div>
                ) : (
                    posts.map(post => <Post key={ post.id } post={ post } refreshPosts={ null } />)
                ) }
            </div>
        </div>
    );
};

export default HashtagPosts;
