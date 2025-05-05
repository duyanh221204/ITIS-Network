import {useState} from "react";
import {useLocation, useNavigate} from "react-router-dom";
import {resetPassword} from "../../../services/authService";
import "../styles.css";

const ResetPassword = () =>
{
    const location = useLocation();
    const navigate = useNavigate();
    const {email} = location.state || {};
    const [newPassword, setNewPassword] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");
    const [error, setError] = useState("");
    const [success, setSuccess] = useState("");
    const [loading, setLoading] = useState(false);

    if (!email)
    {
        navigate("/login");
        return null;
    }

    const handleSubmit = async (e) =>
    {
        e.preventDefault();
        setError("");
        setSuccess("");

        if (newPassword.length < 8)
        {
            setError("Password must be at least 8 characters.");
            return;
        }
        if (newPassword !== confirmPassword)
        {
            setError("Passwords do not match.");
            return;
        }

        setLoading(true);
        try
        {
            const response = await resetPassword(email, newPassword);
            if (response && response.status === "ok")
            {
                setSuccess("Password reset successfully. Redirecting to login...");
                setTimeout(() => navigate("/login"), 2500);
            }
            else
                setError(response?.message || "Failed to reset password.");
        }
        catch (error)
        {
            setError(error?.response?.data?.message || "Failed to reset password.");
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
                <h2>Reset Password</h2>
                <form onSubmit={handleSubmit}>
                    <input
                        type="password"
                        className="input-field"
                        placeholder="New password"
                        value={newPassword}
                        onChange={e => setNewPassword(e.target.value)}
                        required
                    />
                    <input
                        type="password"
                        className="input-field"
                        placeholder="Confirm new password"
                        value={confirmPassword}
                        onChange={e => setConfirmPassword(e.target.value)}
                        required
                    />
                    {
                        error && <div className="error-message">{error}</div>
                    }
                    {
                        success && <div className="success-message">{success}</div>
                    }
                    <button type="submit" className="btn btn-primary" disabled={loading}>
                        {
                            loading ? <div className="loading-spinner"></div> : "Reset Password"
                        }
                    </button>
                </form>
            </div>
        </div>
    );
};

export default ResetPassword;
