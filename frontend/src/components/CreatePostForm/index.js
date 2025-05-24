import { useState, useEffect } from "react";
import { createPost, updatePost } from "../../services/postService";
import { uploadImage } from "../../services/authService";
import { getAllHashtags } from "../../services/hashtagService";
import { useLocation } from "react-router-dom";
import "./styles.css";

const CreatePostForm = ({onPostCreated, mode = "create", initialContent = "", initialImage = "", initialHashtags = [], postId}) =>
{
    const [content, setContent] = useState(initialContent);
    const [image, setImage] = useState(null);
    const [previewUrl, setPreviewUrl] = useState(initialImage);
    const [fileName, setFileName] = useState("");
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");
    const [hashtags, setHashtags] = useState(initialHashtags);
    const [showHashtagModal, setShowHashtagModal] = useState(false);
    const [allHashtags, setAllHashtags] = useState([]);
    const [searchTerm, setSearchTerm] = useState("");
    const [filteredHashtags, setFilteredHashtags] = useState([]);
    const [newHashtagInput, setNewHashtagInput] = useState("");

    const location = useLocation();

    useEffect(() =>
    {
        if (showHashtagModal)
        {
            getAllHashtags().then(res =>
            {
                if (res.status === "ok" && Array.isArray(res.data))
                {
                    setAllHashtags(res.data.map(h => h.name));
                }
            });
        }
    }, [showHashtagModal]);

    useEffect(() =>
    {
        if (searchTerm.trim() === "")
            setFilteredHashtags(allHashtags.filter(h => !hashtags.includes(h)));
        else
        {
            setFilteredHashtags(
                allHashtags.filter(h => h.toLowerCase().includes(searchTerm.toLowerCase()) && !hashtags.includes(h))
            );
        }
    }, [searchTerm, allHashtags, hashtags]);

    useEffect(() =>
    {
        setContent(initialContent);
        setPreviewUrl(initialImage);
        setHashtags(initialHashtags);
    }, [mode, postId]);

    useEffect(() =>
    {
        if (!location.pathname.match(/^\/(create-post|edit-post)/))
        {
            setLoading(false);
            setShowHashtagModal(false);
            setError("");
            setContent("");
            setImage(null);
            setPreviewUrl("");
            setFileName("");
            setHashtags([]);
        }
    }, [location.pathname]);

    const normalizeHashtag = (raw) =>
    {
        let tag = raw.trim().replace(/\s+/g, "");
        if (!tag)
            return null;

        if (!tag.startsWith("#"))
            tag = "#" + tag;
        return tag;
    };

    const handleAddHashtag = (tag) =>
    {
        const norm = normalizeHashtag(tag);
        if (!norm || hashtags.includes(norm))
            return;
        setHashtags([...hashtags, norm]);
        setSearchTerm("");
        setNewHashtagInput("");
        setShowHashtagModal(false);
    };

    const handleRemoveHashtag = (tag) =>
    {
        setHashtags(hashtags.filter(h => h !== tag));
    };

    const handleCreateNewHashtag = () =>
    {
        const norm = normalizeHashtag(newHashtagInput);
        if (!norm || hashtags.includes(norm))
            return;
        setHashtags([...hashtags, norm]);
        setShowHashtagModal(false);
        setNewHashtagInput("");
        setSearchTerm("");
    };

    const handleFileChange = (e) =>
    {
        if (e.target.files && e.target.files[0])
        {
            const file = e.target.files[0];
            setFileName(file.name);
            const reader = new FileReader();
            reader.onload = (e) =>
            {
                setPreviewUrl(e.target.result);
            };
            reader.readAsDataURL(file);
            setImage(file);
        }
    };

    const clearImage = () =>
    {
        setImage(null);
        setPreviewUrl("");
        setFileName("");
    };

    const handleSubmit = async (e) =>
    {
        e.preventDefault();
        if (!content.trim() && !image && !previewUrl)
        {
            setError("Post must have content or image");
            return;
        }

        setLoading(true);
        setError("");
        try
        {
            let imageUrl = previewUrl;
            if (image)
            {
                const imageResponse = await uploadImage(image);
                imageUrl = imageResponse.data;
            }
            if (mode === "edit" && postId)
            {
                await updatePost
                (
                    postId,
                    {
                        content: content.trim(),
                        image: imageUrl,
                        hashtags: hashtags.map(h => h.replace(/^#/, ""))
                    }
                );
            }
            else
            {
                await createPost
                (
                    {
                    content: content.trim(),
                    image: imageUrl,
                    hashtags: hashtags.map(h => h.replace(/^#/, ""))
                    }
                );
            }

            setContent("");
            setImage(null);
            setPreviewUrl("");
            setFileName("");
            setHashtags([]);
            if (onPostCreated)
                onPostCreated();
        }
        catch (error)
        {
            setError(error.response?.data?.message || "Error creating post");
        }
        finally
        {
            setLoading(false);
        }
    };

    return (
        <div className="create-post-form">
            <h3>{mode === "edit" ? "Edit Post" : "Create New Post"}</h3>
            <form onSubmit={handleSubmit}>
                <textarea
                    className="post-textarea"
                    placeholder="What's on your mind?"
                    value={content}
                    onChange={(e) => setContent(e.target.value)}
                ></textarea>

                {
                    hashtags.length > 0 &&
                    (
                        <div className="hashtag-list">
                            {
                                hashtags.map(tag => (
                                    <span className="hashtag-item" key={tag}>
                                        {tag}
                                        <button type="button" className="remove-hashtag" onClick={() => handleRemoveHashtag(tag)}>×</button>
                                    </span>
                                ))
                            }
                        </div>
                    )
                }

                <button type="button" className="btn btn-secondary add-hashtag-btn" onClick={() => setShowHashtagModal(true)}>
                    + Add hashtag
                </button>

                {
                    showHashtagModal &&
                    (
                        <div className="hashtag-modal-overlay" onClick={() => setShowHashtagModal(false)}>
                            <div className="hashtag-modal" onClick={e => e.stopPropagation()}>
                                <h4>Select or create a hashtag</h4>
                                <input
                                    type="text"
                                    className="input-field"
                                    placeholder="Find or create a hashtag"
                                    value={searchTerm}
                                    onChange={e =>
                                    {
                                        setSearchTerm(e.target.value);
                                        setNewHashtagInput(e.target.value);
                                    }}
                                    autoFocus
                                />
                                <div className="hashtag-modal-list">
                                    {
                                        filteredHashtags.length > 0 ?
                                            (
                                                filteredHashtags.map(tag => (
                                                    <div className="hashtag-modal-item" key={tag} onClick={() => handleAddHashtag(tag)}>
                                                        {tag}
                                                    </div>
                                                ))
                                            ) :
                                            (
                                                <div className="hashtag-modal-empty">
                                                    No hashtags found. You can create a new one:
                                                    <button type="button" className="btn btn-primary" style={{marginLeft: 8}} onClick={handleCreateNewHashtag}>
                                                        Add #{newHashtagInput.trim().replace(/\s+/g, "")}
                                                    </button>
                                                </div>
                                            )
                                    }
                                </div>
                                <button type="button" className="btn btn-secondary close-modal-btn" onClick={() => setShowHashtagModal(false)}>
                                    Close
                                </button>
                            </div>
                        </div>
                    )
                }

                {
                    previewUrl &&
                    (
                        <div className="image-preview">
                            <img src={previewUrl} alt="Preview" />
                            <button
                                type="button"
                                className="remove-image"
                                onClick={clearImage}
                            >
                                ×
                            </button>
                        </div>
                    )
                }

                <div className="form-actions">
                    <div className="file-input-container">
                        <label className="file-input-label">
                            <i className="image-icon">🖼️</i>
                            Add Photo
                            <input
                                type="file"
                                className="file-input"
                                accept="image/*"
                                onChange={handleFileChange}
                            />
                        </label>
                        <span className="file-name">{fileName}</span>
                    </div>

                    <button
                        type="submit"
                        className="btn btn-primary post-btn"
                        disabled={loading || (!content.trim() && !image)}
                    >
                        {
                            loading ? <div className="loading-spinner"></div> : "Post"
                        }
                    </button>
                </div>

                {
                    error && <div className="error-message">{error}</div>
                }
            </form>
        </div>
    );
}

export default CreatePostForm;
