import { useState } from "react";
import { createPost } from "../../services/postService";
import { uploadImage } from "../../services/authService";
import "./styles.css";

const CreatePostForm = ({onPostCreated}) =>
{
    const [content, setContent] = useState("");
    const [image, setImage] = useState(null);
    const [previewUrl, setPreviewUrl] = useState("");
    const [fileName, setFileName] = useState("");
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

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

        if (!content.trim() && !image)
        {
            setError("Post must have content or image");
            return;
        }

        setLoading(true);
        setError("");

        try
        {
            let imageUrl = null;
            if (image)
            {
                const imageResponse = await uploadImage(image);
                imageUrl = imageResponse.data;
            }

            await createPost
            (
                {
                    content: content.trim(),
                    image: imageUrl
                }
            );

            setContent("");
            setImage(null);
            setPreviewUrl("");
            setFileName("");

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
            <h3>Create New Post</h3>
            <form onSubmit={handleSubmit}>
        <textarea
            className="post-textarea"
            placeholder="What's on your mind?"
            value={content}
            onChange={(e) => setContent(e.target.value)}
        ></textarea>

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
