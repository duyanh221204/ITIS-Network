import {useState, useEffect} from "react";
import {useLocation, useNavigate} from "react-router-dom";
import {sendOtp} from "../../../services/authService";
import "../styles.css";

const OtpVerify = () =>
{
    const location = useLocation();
    const navigate = useNavigate();
    const {email, type} = location.state || {};
    const [otp, setOtp] = useState("");
    const [error, setError] = useState("");
    const [success, setSuccess] = useState("");
    const [loading, setLoading] = useState(false);
    const [timer, setTimer] = useState(300);
    const [canResend, setCanResend] = useState(false);
    const [serverOtp, setServerOtp] = useState("");
    const [firstLoad, setFirstLoad] = useState(true);

    useEffect(() =>
    {
        if (!email)
            navigate("/login");
    }, [email, navigate]);

    useEffect(() =>
    {
        let interval = null;
        if (timer > 0)
            interval = setInterval(() => setTimer(t => t - 1), 1000);
        else
            setCanResend(true);
        return () => clearInterval(interval);
    }, [timer]);

    useEffect(() =>
    {
        if (firstLoad)
        {
            handleResend();
            setFirstLoad(false);
        }
    }, [firstLoad]);

    const handleResend = async () =>
    {
        setError("");
        setSuccess("");
        setLoading(true);
        setTimer(300);
        setCanResend(false);
        try
        {
            const response = await sendOtp(email);
            if (response && response.status === "ok")
            {
                setServerOtp(response.data);
                setSuccess("OTP sent to your email.");
            }
            else
                setError(response?.message || "Failed to send OTP.");
        }
        catch (error)
        {
            setError(error?.response?.data?.message || "Failed to send OTP.");
        }
        finally
        {
            setLoading(false);
        }
    };

    const handleSubmit = (e) =>
    {
        e.preventDefault();
        setError("");
        setSuccess("");
        if (otp.length !== 6)
        {
            setError("OTP must be 6 digits.");
            return;
        }
        if (otp === serverOtp)
        {
            if (type === "reset")
                navigate("/reset-password",
                    {
                        state: {email}
                    }
                );
            else
                navigate("/login",
                    {
                        state:
                            {
                                email,
                                verified: true
                            }
                    }
                );
        }
        else
        {
            setError("Incorrect OTP. Please request a new code.");
            setOtp("");
            setCanResend(true);
            setTimer(0);
        }
    };

    const formatTime = (t) =>
    {
        const m = Math.floor(t / 60);
        const s = t % 60;
        return `${m}:${s.toString().padStart(2, "0")}`;
    };

    return (
        <div className="auth-container">
            <div className="auth-box">
                <img src="/logo.jfif" alt="Logo" className="auth-logo" />
                <h2>Verify OTP</h2>
                <p className="otp-instruction">Enter the 6-digit code sent to <b>{email}</b></p>
                <form onSubmit={ handleSubmit }>
                    <input
                        type="text"
                        className="input-field"
                        placeholder="Enter OTP"
                        value={ otp }
                        onChange={ e => setOtp(e.target.value.replace(/\D/g, "").slice(0, 6)) }
                        required
                    />
                    {
                        timer > 0 &&
                        (
                            <div className="otp-timer">Resend code in {formatTime(timer)}</div>
                        )
                    }
                    {
                        canResend &&
                        (
                            <button type="button" className="btn btn-secondary" onClick={handleResend} disabled={loading}>
                                {
                                    loading ? <div className="loading-spinner"></div> : "Resend OTP"
                                }
                            </button>
                        )
                    }
                    {
                        error && <div className="error-message">{error}</div>
                    }
                    {
                        success && <div className="success-message">{success}</div>
                    }
                    <button type="submit" className="btn btn-primary" disabled={loading}>
                        Verify
                    </button>
                </form>
            </div>
        </div>
    );
};

export default OtpVerify;
