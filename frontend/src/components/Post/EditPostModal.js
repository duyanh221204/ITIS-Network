import { useState, useEffect } from "react";
import { updatePost } from "../../services/postService";
import { uploadImage } from "../../services/authService";
import "./styles.css";

const EditPostModal = ({ post, onClose, onUpdated }) =>
{
    const [content, setContent] = useState(post.content || "");
    const [hashtags, setHashtags] = useState(post.hashtags ? post.hashtags.map(h => `#${ h.name }`) : []);
    const [image, setImage] = useState(null);
    const [previewUrl, setPreviewUrl] = useState(post.image || "");
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    useEffect(() =>
    {
        setContent(post.content || "");
        setHashtags(post.hashtags ? post.hashtags.map(h => `#${ h.name }`) : []);
        setPreviewUrl(post.image || "");
    }, [post]);

    const handleFileChange = (e) =>
    {
        if (e.target.files && e.target.files[0])
        {
            const file = e.target.files[0];
            const reader = new FileReader();
            reader.onload = (e) =>
            {
                setPreviewUrl(e.target.result);
            };
            reader.readAsDataURL(file);
            setImage(file);
        }
    };

    const handleSubmit = async (e) =>
    {
        e.preventDefault();
        setLoading(true);
        setError("");
        try
        {
            let imageUrl = post.image;
            if (image)
            {
                const imageResponse = await uploadImage(image);
                imageUrl = imageResponse.data;
            }
            const payload = {
                content: content.trim(),
                image: imageUrl,
                hashtags: hashtags.map(h => h.replace(/^#/, "")),
            };
            await updatePost(post.id, payload);
            if (onUpdated) onUpdated();
            onClose();
        } catch (err)
        {
            setError(err.response?.data?.message || "Error updating post");
        } finally
        {
            setLoading(false);
        }
    };

    return (
        <div className="modal-overlay" onClick={ onClose }>
            <div className="modal edit-post-modal" onClick={ e => e.stopPropagation() }>
                <div className="modal-header">
                    <h3>Edit Post</h3>
                    <button className="modal-close" onClick={ onClose }>×</button>
                </div>
                <form onSubmit={ handleSubmit }>
                    <textarea
                        className="post-textarea"
                        value={ content }
                        onChange={ e => setContent(e.target.value) }
                        required
                    ></textarea>
                    {/* Hashtag editing (simple, can be improved) */ }
                    <div className="hashtag-list">
                        { hashtags.map(tag => (
                            <span className="hashtag-item" key={ tag }>
                                { tag }
                                <button type="button" className="remove-hashtag" onClick={ () => setHashtags(hashtags.filter(h => h !== tag)) }>×</button>
                            </span>
                        )) }
                        <input
                            type="text"
                            className="input-field"
                            placeholder="#hashtag"
                            onKeyDown={ e =>
                            {
                                if (e.key === "Enter" && e.target.value.trim())
                                {
                                    const val = e.target.value.trim();
                                    if (!hashtags.includes(val.startsWith("#") ? val : `#${ val }`))
                                    {
                                        setHashtags([...hashtags, val.startsWith("#") ? val : `#${ val }`]);
                                    }
                                    e.target.value = "";
                                    e.preventDefault();
                                }
                            } }
                        />
                    </div>
                    { previewUrl && (
                        <div className="image-preview">
                            <img src={ previewUrl } alt="Preview" />
                            <button type="button" className="remove-image" onClick={ () => { setPreviewUrl(""); setImage(null); } }>×</button>
                        </div>
                    ) }
                    <label className="file-input-label">
                        <i className="image-icon">🖼️</i> Change Photo
                        <input type="file" className="file-input" accept="image/*" onChange={ handleFileChange } />
                    </label>
                    { error && <div className="error-message">{ error }</div> }
                    <button type="submit" className="btn btn-primary" disabled={ loading }>{ loading ? "Saving..." : "Save Changes" }</button>
                </form>
            </div>
        </div>
    );
};

export default EditPostModal;
