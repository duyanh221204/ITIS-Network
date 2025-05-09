import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { likePost, unlikePost, createComment } from "../../services/postService";
import "./styles.css";

const Post = ({post}) =>
{
    const [showComments, setShowComments] = useState(false);
    const [showLikes, setShowLikes] = useState(false);
    const [commentText, setCommentText] = useState("");
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [isLiking, setIsLiking] = useState(false);
    const [localLikes, setLocalLikes] = useState(post.likes ? post.likes.length : 0);
    const [localHasLiked, setLocalHasLiked] = useState(
        post.likes ? post.likes.some(like => like.liker_id === parseInt(localStorage.getItem("userId"))) : false
    );
    const [localComments, setLocalComments] = useState(post.comments || []);
    const [localLikesList, setLocalLikesList] = useState(post.likes || []);
    const [pendingComments, setPendingComments] = useState([]);

    useEffect(() =>
    {
        setLocalLikesList(post.likes || []);
        setLocalLikes(post.likes ? post.likes.length : 0);
        setLocalHasLiked(post.likes ? post.likes.some(like => like.liker_id === parseInt(localStorage.getItem("userId"))) : false);
        setLocalComments(
            [
                ...post.comments,
                ...pendingComments.filter
                (
                    pc => !post.comments.some(c => c.id === pc.id)
                )
            ]
        );
    }, [pendingComments, post.comments, post.likes]);

    const toggleComments = () =>
    {
        setShowComments(!showComments);
        setShowLikes(false);
    };

    const toggleLikes = () =>
    {
        setShowLikes(!showLikes);
        setShowComments(false);
    };

    const handleLikeUnlike = async () =>
    {
        if (isLiking)
            return;

        setIsLiking(true);
        try
        {
            const userId = parseInt(localStorage.getItem("userId"));
            const userName = localStorage.getItem("username");
            const userAvatar = localStorage.getItem("avatar");

            if (localHasLiked)
            {
                setLocalLikes(l => l - 1);
                setLocalHasLiked(false);
                setLocalLikesList(likes => likes.filter(like => like.liker_id !== userId));
                await unlikePost(post.id);
            }
            else
            {
                setLocalLikes(l => l + 1);
                setLocalHasLiked(true);
                setLocalLikesList(likes =>
                    [
                        ...likes,
                        {
                            id: Date.now(),
                            liker_id: userId,
                            liker_name: userName || "You",
                            liker_avatar: userAvatar || "/default_avatar.png"
                        }
                    ]
                );
                await likePost(post.id);
            }
        }
        catch (error)
        {
            setLocalLikes(localHasLiked ? l => l + 1 : l => l - 1);
            setLocalHasLiked(h => !h);
            throw error;
        }
        finally
        {
            setIsLiking(false);
        }
    };

    const handleCommentSubmit = async (e) =>
    {
        e.preventDefault();
        if (!commentText.trim() || isSubmitting)
            return;
        setIsSubmitting(true);

        try
        {
            const tempId = "pending-" + Date.now();
            const userId = parseInt(localStorage.getItem("userId"));
            const userName = localStorage.getItem("username") || "You";
            const userAvatar = localStorage.getItem("avatar") || "/default_avatar.png";
            const tempComment =
                {
                    id: tempId,
                    author_id: userId,
                    author_name: userName,
                    author_avatar: userAvatar,
                    content: commentText,
                };

            setPendingComments(pending => [...pending, tempComment]);
            setLocalComments(comments => [...comments, tempComment]);
            setCommentText("");

            const response = await createComment
            (
                {
                    content: tempComment.content,
                    post_id: post.id
                }
            );
            if (response.status === "ok" && response.data)
            {
                setPendingComments(pending => pending.filter(c => c.id !== tempId));
                setLocalComments(comments =>
                    [
                        ...comments.filter(c => c.id !== tempId),
                        response.data
                    ]
                );
            }
        }
        catch (error)
        {
            setPendingComments(pending => pending.slice(0, -1));
            setLocalComments(comments => comments.slice(0, -1));
            throw error;
        }
        finally
        {
            setIsSubmitting(false);
        }
    };

    const formatDate = (dateString) =>
    {
        const date = new Date(dateString);
        return date.toLocaleString();
    };

    return (
        <div className="post">
            <div className="post-header">
                <Link to={`/profile/${post.author_id}`} className="author-info">
                    <img
                        src={post.author_avatar || "/default_avatar.png"}
                        alt={post.author_name}
                        className="author-avatar"
                    />
                    <span className="author-name">{post.author_name}</span>
                </Link>
                <span className="post-date">{formatDate(post.created_at)}</span>
            </div>

            {
                post.image &&
                (
                    <div className="post-image">
                        <img src={post.image} alt="Post content" />
                    </div>
                )
            }

            {
                post.content &&
                (
                    <div className="post-content">
                        <p>{post.content}</p>
                    </div>
                )
            }

            <div className="post-actions">
                <button
                    className={`post-action ${localHasLiked ? "liked" : ""}`}
                    onClick={handleLikeUnlike}
                >
                    <span>{localHasLiked ? "❤️" : "🤍"}</span>
                </button>
                <button className="post-action" onClick={toggleLikes}>
                    <span className="action-text">{localLikes} Likes</span>
                </button>
                <button className="post-action" onClick={toggleComments}>
                    <span>💬</span>
                    <span className="action-text">{localComments.length} Comments</span>
                </button>
            </div>

            {
                showLikes && localLikesList.length > 0 &&
                (
                    <div className="modal-overlay" onClick={toggleLikes}>
                        <div className="modal likes-modal" onClick={e => e.stopPropagation()}>
                            <div className="modal-header">
                                <h4>Likes</h4>
                                <button className="modal-close" onClick={toggleLikes}>×</button>
                            </div>
                            <ul className="likes-list">
                                {
                                    localLikesList.map(like =>
                                        (
                                            <li key={like.id} className="like-item">
                                                <Link to={`/profile/${like.liker_id}`} className="like-user">
                                                    <img
                                                        src={like.liker_avatar || "/default_avatar.png"}
                                                        alt={like.liker_name}
                                                        className="like-avatar"
                                                    />
                                                    <span className="like-username">{like.liker_name}</span>
                                                </Link>
                                            </li>
                                        )
                                    )
                                }
                            </ul>
                        </div>
                    </div>
                )
            }

            {
                showComments &&
                (
                    <div className="comments-container">
                        <form className="comment-form" onSubmit={handleCommentSubmit}>
                            <input
                                type="text"
                                className="comment-input"
                                placeholder="Write a comment..."
                                value={commentText}
                                onChange={(e) => setCommentText(e.target.value)}
                            />
                            <button
                                type="submit"
                                className="comment-submit"
                                disabled={!commentText.trim() || isSubmitting}
                            >
                                {
                                    isSubmitting ? "..." : "Post"
                                }
                            </button>
                        </form>

                        {
                            localComments.length > 0 ?
                                (
                                    <ul className="comments-list">
                                        {
                                            localComments.map(comment =>
                                                (
                                                    <li key={comment.id} className="comment-item">
                                                        <Link to={`/profile/${comment.author_id}`} className="comment-author">
                                                            <img
                                                                src={comment.author_avatar || "/default_avatar.png"}
                                                                alt={comment.author_name}
                                                                className="comment-avatar"
                                                            />
                                                        </Link>
                                                        <div className="comment-content">
                                                            <Link to={`/profile/${comment.author_id}`} className="comment-author-name">
                                                                {
                                                                    comment.author_name
                                                                }
                                                            </Link>
                                                            <p className="comment-text">{comment.content}</p>
                                                        </div>
                                                    </li>
                                                )
                                            )
                                        }
                                    </ul>
                                ) :
                                (
                                    <p className="no-comments">No comments yet. Be the first to comment!</p>
                                )
                        }
                    </div>
                )
            }
        </div>
    );
}

export default Post;
