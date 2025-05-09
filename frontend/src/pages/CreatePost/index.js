import { useNavigate } from "react-router-dom";
import CreatePostForm from "../../components/CreatePostForm";
import "./styles.css";

const CreatePost = () =>
{
    const navigate = useNavigate();

    const handlePostCreated = () =>
    {
        navigate("/");
    };

    return (
        <div className="create-post-page">
            <h1 className="page-title">Create Post</h1>
            <div className="create-post-container">
                <CreatePostForm onPostCreated={handlePostCreated} />
            </div>
        </div>
    );
}

export default CreatePost;
