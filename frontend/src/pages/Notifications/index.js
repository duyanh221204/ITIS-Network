import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { getAllNotifications, markNotificationAsRead } from "../../services/notificationService";
import "./styles.css";

const Notifications = () =>
{
    const [notifications, setNotifications] = useState([]);
    const [loading, setLoading] = useState(true);
    const navigate = useNavigate();

    useEffect(() =>
    {
        const fetchData = async () =>
        {
            setLoading(true);
            const res = await getAllNotifications();
            if (res.status === "ok" && Array.isArray(res.data))
            {
                setNotifications(res.data);
            }
            setLoading(false);
        };
        fetchData();
    }, []);

    const handleNotificationClick = async (notification) =>
    {
        if (!notification.is_read)
        {
            await markNotificationAsRead(notification.id);
            setNotifications(notifications.map(n => n.id === notification.id ? { ...n, is_read: true } : n));
        }
        if (notification.type === "follow")
        {
            navigate(`/profile/${ notification.actor.id }`);
        } else if (notification.type === "like" || notification.type === "comment")
        {
            navigate(`/post/${ notification.post_id }`);
        }
    };

    if (loading) return <div className="loading"><div className="loading-spinner"></div></div>;

    return (
        <div className="notifications-page">
            <h1 className="page-title">All Notifications</h1>
            <div className="notifications-list-container">
                { notifications.length === 0 ? (
                    <p className="empty-message">No notifications yet</p>
                ) : (
                    <ul className="notifications-list-full">
                        { notifications.map(notification => (
                            <li
                                key={ notification.id }
                                className={ `notification-item ${ !notification.is_read ? "unread" : "" }` }
                                onClick={ () => handleNotificationClick(notification) }
                            >
                                <span className="notification-time-top">
                                    { new Date(notification.created_at).toLocaleString() }
                                </span>
                                <div className="notification-content">
                                    { notification.actor && (
                                        <img
                                            src={ notification.actor.avatar || "/default_avatar.png" }
                                            alt={ notification.actor.username }
                                            className="notification-avatar"
                                        />
                                    ) }
                                    <p>
                                        { notification.actor ? <strong>{ notification.actor.username }</strong> : "Someone" } { " " }
                                        { notification.type === "follow" && "started following you" }
                                        { notification.type === "like" && "liked your post" }
                                        { notification.type === "comment" && "commented on your post" }
                                    </p>
                                </div>
                                { !notification.is_read && <span className="unread-indicator"></span> }
                            </li>
                        )) }
                    </ul>
                ) }
            </div>
        </div>
    );
};

export default Notifications;
