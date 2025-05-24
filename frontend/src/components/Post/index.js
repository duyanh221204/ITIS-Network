import { useState, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import { likePost, unlikePost, createComment, deletePost, deleteComment } from "../../services/postService";
import "./styles.css";
import EditPostModal from "./EditPostModal";

const Post = ({post, refreshPosts}) =>
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
    const [showImageModal, setShowImageModal] = useState(false);
    const [showCommentModal, setShowCommentModal] = useState(false);
    const [showEditModal, setShowEditModal] = useState(false);
    const currentUserId = parseInt(localStorage.getItem("userId"));
    const navigate = useNavigate();

    useEffect(() =>
    {
        const userId = parseInt(localStorage.getItem("userId"));
        setLocalLikesList(Array.isArray(post.likes) ? post.likes.map(like => (
            {
                ...like,
                liker_name: like.liker_name || like.liker_username || "You",
                liker_avatar: like.liker_avatar && like.liker_avatar !== "null" && like.liker_avatar !== "undefined" ? like.liker_avatar : "/default_avatar.png"
            }
        )) : []);
        setLocalLikes(Array.isArray(post.likes) ? post.likes.length : 0);
        let hasLiked = Array.isArray(post.likes) ? post.likes.some(like => like.liker_id === userId) : false;
        if (!hasLiked)
        {
            const likedPosts = JSON.parse(localStorage.getItem("likedPosts") || "[]");
            hasLiked = likedPosts.includes(post.id);
        }
        setLocalHasLiked(hasLiked);
    }, [post.likes, post.id]);

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
            let userName = localStorage.getItem("username");
            let userAvatar = localStorage.getItem("avatar");

            if (!userName || userName === "null" || userName === "undefined")
                userName = "You";
            if (!userAvatar || userAvatar === "null" || userAvatar === "undefined")
                userAvatar = "/default_avatar.png";

            let likedPosts = JSON.parse(localStorage.getItem("likedPosts") || "[]");

            if (localHasLiked)
            {
                setLocalLikes(l => Math.max(0, l - 1));
                setLocalHasLiked(false);
                setLocalLikesList(likes => likes.filter(like => like.liker_id !== userId));
                await unlikePost(post.id);
                likedPosts = likedPosts.filter(id => id !== post.id);
                localStorage.setItem("likedPosts", JSON.stringify(likedPosts));
            }
            else
            {
                const response = await likePost(post.id);
                let likeObj = response && response.data ? response.data : null;
                if (!likeObj)
                {
                    likeObj = {
                        id: Date.now(),
                        liker_id: userId,
                        liker_name: userName,
                        liker_avatar: userAvatar,
                        post_id: post.id,
                        post_author_id: post.author_id
                    };
                }
                setLocalLikes(l => l + 1);
                setLocalHasLiked(true);
                setLocalLikesList(likes =>
                {
                    if (likes.some(like => like.liker_id === userId))
                    {
                        return likes.map(like => like.liker_id === userId ? likeObj : like);
                    }
                    return [
                        ...likes,
                        likeObj
                    ];
                });

                if (!likedPosts.includes(post.id))
                {
                    likedPosts.push(post.id);
                    localStorage.setItem("likedPosts", JSON.stringify(likedPosts));
                }
            }
        }
        catch (error)
        {
            setLocalLikes(localHasLiked ? l => l + 1 : l => Math.max(0, l - 1));
            setLocalHasLiked(h => !h);
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
                    comments.map(c =>
                        c.id === tempId ? {...response.data} : c
                    )
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

    const handleDeletePost = async () =>
    {
        if (window.confirm("Are you sure you want to delete this post?"))
        {
            await deletePost(post.id);
            if (refreshPosts) refreshPosts();
        }
    };

    const handleDeleteComment = async (commentId) =>
    {
        if (window.confirm("Are you sure you want to delete this comment?"))
        {
            await deleteComment(commentId);
            setLocalComments(localComments.filter(c => c.id !== commentId));
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
                <div className="post-header-actions">
                    {
                        post.author_id === currentUserId &&
                        (
                            <>
                                <button className="post-edit-icon" title="Edit" onClick={() => navigate(`/edit-post/${post.id}`)}>
                                    <span role="img" aria-label="edit">✏️</span>
                                </button>
                                <button className="post-delete-icon" title="Delete" onClick={handleDeletePost}>
                                    <span role="img" aria-label="delete">🗑️</span>
                                </button>
                            </>
                        )
                    }
                    <span className="post-date">{formatDate(post.created_at)}</span>
                </div>
            </div>

            {
                post.image &&
                (
                    <div className="post-image" onClick={() => setShowImageModal(true)} style={{cursor: "pointer"}}>
                        <img src={post.image} alt="Post content" />
                    </div>
                )
            }

            {
                showImageModal &&
                (
                    <div className="image-modal-overlay" onClick={() => setShowImageModal(false)}>
                        <div className="image-modal" onClick={e => e.stopPropagation()}>
                            <img src={post.image} alt="Full" className="image-modal-img" />
                            <button className="image-modal-close" onClick={() => setShowImageModal(false)}>×</button>
                        </div>
                    </div>
                )
            }

            {
                post.content &&
                (
                    <div className="post-content">
                        <p style={{whiteSpace: "pre-line"}}>{post.content}</p>
                        {
                            post.hashtags && post.hashtags.length > 0 &&
                            (
                                <div className="post-hashtags">
                                    {
                                        post.hashtags.map((h, idx) => (
                                            <span
                                                className="post-hashtag"
                                                key={h.id}
                                                style={{cursor: "pointer"}}
                                                onClick={() => navigate(`/hashtag/${encodeURIComponent(h.name)}`)}
                                            >
                                                #{h.name}{idx !== post.hashtags.length - 1 ? " " : ""}
                                            </span>
                                        ))
                                    }
                                </div>
                            )
                        }
                    </div>
                )
            }

            <div className="post-actions">
                <button
                    className={`post-action${localHasLiked ? " liked" : ""}`}
                    onClick={handleLikeUnlike}
                >
                    <span className="icon-like">{localHasLiked ? "❤️" : "🤍"}</span>
                    <span className="action-text">{localLikes}</span>
                </button>
                <button className="post-action-btn" onClick={toggleLikes}>
                    <span className="action-text">View likes</span>
                </button>
                <button className="post-action-btn" onClick={() => setShowCommentModal(true)}>
                    <span className="icon-comment">💬</span>
                    <span className="action-text">{localComments.length}</span>
                </button>
            </div>

            {
                showLikes && localLikesList.length > 0 &&
                (
                    <div className="modal-overlay" onClick={toggleLikes}>
                        <div className="modal likes-modal" onClick={e => e.stopPropagation()}>
                            <div className="modal-header">
                                <h4 style={{color: "var(--primary-color)"}}>Likes</h4>
                                <button className="modal-close" onClick={toggleLikes}>×</button>
                            </div>
                            <ul className="likes-list">
                                {
                                    localLikesList.map(like => (
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
                                    ))
                                }
                            </ul>
                        </div>
                    </div>
                )
            }

            {
                showCommentModal &&
                (
                    <div className="comment-modal-overlay" onClick={() => setShowCommentModal(false)}>
                        <div className="comment-modal" onClick={e => e.stopPropagation()}>
                            <div className="comment-modal-header">
                                <h3>Comments</h3>
                                <button className="comment-modal-close" onClick={() => setShowCommentModal(false)}>×</button>
                            </div>
                            <div className="comment-modal-list">
                                {
                                    localComments.length > 0 ?
                                        (
                                            localComments.map(c => (
                                                <div className="comment-item" key={c.id}>
                                                    <img src={c.author_avatar || "/default_avatar.png"} alt={c.author_name} className="comment-avatar" />
                                                    <div className="comment-content-block">
                                                <span className="comment-author">
                                                    <Link to={`/profile/${c.author_id}`}>{c.author_name}</Link>
                                                </span>
                                                        <span className="comment-content">{ c.content }</span>
                                                        {
                                                            (c.author_id === currentUserId || post.author_id === currentUserId) &&
                                                            (
                                                                <button
                                                                    className="comment-delete-btn"
                                                                    title="Delete comment"
                                                                    onClick={() => handleDeleteComment(c.id)}
                                                                >
                                                                    🗑️
                                                                </button>
                                                            )
                                                        }
                                                    </div>
                                                </div>
                                            ))
                                        ) :
                                        (
                                            <div className="comment-empty">No comments yet. Be the first to comment!</div>
                                        )
                                }
                            </div>
                            <form className="comment-modal-input-row" onSubmit={handleCommentSubmit}>
                                <input
                                    type="text"
                                    className="comment-modal-input"
                                    placeholder="Write a comment..."
                                    value={commentText}
                                    onChange={e => setCommentText(e.target.value)}
                                    disabled={isSubmitting}
                                />
                                <button type="submit" className="btn btn-primary" disabled={isSubmitting || !commentText.trim()}>
                                    Send
                                </button>
                            </form>
                        </div>
                    </div>
                )
            }

            {
                showLikes && localLikesList.length > 0 &&
                (
                    <div className="modal-overlay" onClick={toggleLikes}>
                        <div className="modal likes-modal" onClick={e => e.stopPropagation()}>
                            <div className="modal-header">
                                <h4 style={{color: "var(--primary-color)"}}>Likes</h4>
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
                                                    {
                                                        (comment.author_id === currentUserId || post.author_id === currentUserId) &&
                                                        (
                                                            <button
                                                                className="comment-delete-btn"
                                                            title="Delete comment"
                                                            onClick={() => handleDeleteComment(comment.id)}
                                                            >
                                                                🗑️
                                                            </button>
                                                        )
                                                    }
                                                </li>
                                            ))
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
            {
                showEditModal &&
                (
                    <EditPostModal post={post} onClose={() => setShowEditModal(false)} onUpdated={refreshPosts} />
                )
            }
        </div>
    );
}

export default Post;
