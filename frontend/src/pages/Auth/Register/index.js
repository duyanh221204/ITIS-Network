import {useState} from "react";
import {Link, useNavigate} from "react-router-dom";
import {register, uploadImage} from "../../../services/authService";
import "../styles.css";

const Register = () =>
{
    const [formData, setFormData] = useState(
        {
            username: "",
            email: "",
            password: "",
            confirmPassword: "",
            introduction: "",
            avatar: null
        }
    );
    const [fileName, setFileName] = useState("");
    const [previewUrl, setPreviewUrl] = useState("");
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    const handleChange = (e) =>
    {
        const {name, value} = e.target;
        setFormData
            (
                {
                    ...formData,
                    [name]: value
                }
            );
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

            setFormData
                (
                    {
                        ...formData,
                        avatar: file
                    }
                );
        }
    };

    const handleSubmit = async (e) =>
    {
        e.preventDefault();
        setError("");

        if (formData.password.length < 8)
        {
            setError("Password must be at least 8 characters.");
            return;
        }
        if (formData.password !== formData.confirmPassword)
        {
            setError("Passwords don't match");
            return;
        }
        setLoading(true);

        try
        {
            let avatarUrl = null;
            if (formData.avatar)
            {
                const imageResponse = await uploadImage(formData.avatar);
                avatarUrl = imageResponse.data;
            }

            const response = await register
                (
                    {
                        username: formData.username,
                        email: formData.email,
                        password: formData.password,
                        avatar: avatarUrl,
                        introduction: formData.introduction
                    }
                );
            if (response && response.status === "ok")
                navigate("/verify-otp",
                    {
                        state:
                            {
                                email: formData.email,
                                type: "register"
                            }
                    }
                );
            else
                setError(response?.message || "Registration failed");
        }
        catch (error)
        {
            setError(error.response?.data?.message || error.message || "Registration failed");
        }
        finally
        {
            setLoading(false);
        }
    };

    return (
        <div className="auth-container">
            <div className="auth-box">
                <img src="/logo.jfif" alt="Logo" className="auth-logo" />
                <h2>Register</h2>
                <form onSubmit={handleSubmit}>
                    <input
                        type="text"
                        name="username"
                        className="input-field"
                        placeholder="Username"
                        value={formData.username}
                        onChange={handleChange}
                        required
                    />
                    <input
                        type="email"
                        name="email"
                        className="input-field"
                        placeholder="Email"
                        value={formData.email}
                        onChange={handleChange}
                        required
                    />
                    <textarea
                        name="introduction"
                        className="input-field"
                        placeholder="Introduction (optional)"
                        value={formData.introduction}
                        onChange={handleChange}
                    />
                    <div className="file-input-container">
                        <label className="file-input-label">
                            Upload Avatar
                            <input
                                type="file"
                                className="file-input"
                                accept="image/*"
                                onChange={handleFileChange}
                            />
                        </label>
                        <span className="file-name">{fileName}</span>
                        {
                            previewUrl &&
                            (
                                <div style={{marginTop: "8px"}}>
                                    <img
                                        src={previewUrl}
                                        alt="Avatar preview"
                                        style={{width: "100px", height: "100px", objectFit: "cover", borderRadius: "50%"}}
                                    />
                                </div>
                            )
                        }
                    </div>
                    <input
                        type="password"
                        name="password"
                        className="input-field"
                        placeholder="Password"
                        value={formData.password}
                        onChange={handleChange}
                        required
                    />
                    <input
                        type="password"
                        name="confirmPassword"
                        className="input-field"
                        placeholder="Confirm Password"
                        value={formData.confirmPassword}
                        onChange={handleChange}
                        required
                    />
                    {
                        error && <div className="error-message">{error}</div>
                    }
                    <button type="submit" className="btn btn-primary" disabled={loading}>
                        {
                            loading ? <div className="loading-spinner"></div> : "Register"
                        }
                    </button>
                </form>
                <p className="auth-footer">
                    Already have an account? <Link to="/login">Login</Link>
                </p>
            </div>
        </div>
    );
}

export default Register;
