import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import Post from "../../components/Post";
import { getAllPosts } from "../../services/postService";
import "../Home/styles.css";

const PostDetail = () =>
{
    const {postId} = useParams();
    const [post, setPost] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() =>
    {
        const fetchPost = async () =>
        {
            setLoading(true);
            const res = await getAllPosts();
            if (res.status === "ok" && Array.isArray(res.data))
            {
                const found = res.data.find(p => String(p.id) === String(postId));
                setPost(found);
            }
            setLoading(false);
        };
        fetchPost();
    }, [postId]);

    if (loading)
        return <div className="loading"><div className="loading-spinner"></div></div>;
    if (!post)
        return <div className="error-message">Post not found.</div>;

    return (
        <div className="news-feed-page">
            <div className="news-feed-container" style={{maxWidth: 600, margin: "32px auto"}}>
                <Post post={post} refreshPosts={null} />
            </div>
        </div>
    );
};

export default PostDetail;
