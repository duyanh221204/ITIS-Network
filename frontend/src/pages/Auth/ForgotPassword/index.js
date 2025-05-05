import {useState} from "react";
import {useNavigate} from "react-router-dom";
import {sendOtp} from '../../../services/authService';
import '../styles.css';

const ForgotPassword = () =>
{
    const [email, setEmail] = useState("");
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);
    const [success, setSuccess] = useState("");
    const navigate = useNavigate();

    const handleSubmit = async (e) =>
    {
        e.preventDefault();
        setError("");
        setSuccess("");
        setLoading(true);

        try
        {
            const response = await sendOtp(email);
            if (response && response.status === "ok")
            {
                setSuccess("OTP sent to your email.");
                setTimeout(() =>
                {
                    navigate("/verify-otp",
                        {
                            state:
                                {
                                    email,
                                    type: "reset"
                                }
                        }
                    );
                }, 1000);
            }
            else
            {
                setError(response?.message || "Failed to send OTP.");
            }
        }
        catch (err)
        {
            setError(err?.response?.data?.message || "Failed to send OTP.");
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
                <h2>Forgot Password</h2>
                <form onSubmit={handleSubmit}>
                    <input
                        type="email"
                        className="input-field"
                        placeholder="Enter your email"
                        value={email}
                        onChange={e => setEmail(e.target.value)}
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
                            loading ? <div className="loading-spinner"></div> : "Send OTP"
                        }
                    </button>
                </form>
            </div>
        </div>
    );
};

export default ForgotPassword;
