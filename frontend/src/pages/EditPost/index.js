import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import CreatePostForm from "../../components/CreatePostForm";
import { getAllPosts } from "../../services/postService";
import "../CreatePost/styles.css";

const EditPost = () =>
{
    const { postId } = useParams();
    const navigate = useNavigate();
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
        <div className="create-post-page">
            <h1 className="page-title">Edit Post</h1>
            <div className="create-post-container">
                <CreatePostForm
                    mode="edit"
                    initialContent={post.content}
                    initialImage={post.image}
                    initialHashtags={post.hashtags ? post.hashtags.map(h => `#${h.name}`) : []}
                    postId={post.id}
                    onPostCreated={() => navigate(`/profile/${post.author_id}`)}
                />
            </div>
        </div>
    );
};

export default EditPost;
