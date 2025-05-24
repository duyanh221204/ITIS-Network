import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { login } from "../../../services/authService";
import "./styles.css";

const Login = ({ setIsAuthenticated }) =>
{
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    const handleSubmit = async (e) =>
    {
        e.preventDefault();
        setError("");
        setLoading(true);

        try
        {
            const response = await login(username, password);
            if (response && response.access_token)
            {
                localStorage.setItem("token", response.access_token);
                setIsAuthenticated(true);
                navigate("/");
            }
            else
            {
                setError("Incorrect username or password");
            }
        }
        catch (error)
        {
            setError(error.response?.data?.message || "Login failed");
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
                <h2>Login</h2>
                <p className="auth-note">Login to share your moments and connect with people!</p>
                <form onSubmit={handleSubmit}>
                    <input
                        type="text"
                        className="input-field"
                        placeholder="Username"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        required
                    />
                    <input
                        type="password"
                        className="input-field"
                        placeholder="Password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                    />
                    {
                        error && <div className="error-message">{error}</div>
                    }
                    <button type="submit" className="btn btn-primary" disabled={loading}>
                        {
                            loading ? <div className="loading-spinner"></div> : "Login"
                        }
                    </button>
                </form>
                <p className="auth-footer">
                    Don't have an account? <Link to="/register">Register</Link>
                    <br />
                    <Link to="/forgot-password" className="forgot-link">Forgot your password?</Link>
                </p>
            </div>
        </div>
    );
}

export default Login;
