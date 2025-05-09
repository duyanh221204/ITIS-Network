import { useState, useEffect, useRef } from "react";
import { Link, useNavigate } from "react-router-dom";
import { getAllNotifications, markNotificationAsRead, getNotificationWsUrl } from "../../services/notificationService";
import { getAllConversations, getUnreadConversations } from "../../services/chatService";
import "./styles.css";

const Header = () =>
{
    const [showNotifications, setShowNotifications] = useState(false);
    const [showMessages, setShowMessages] = useState(false);
    const [notifications, setNotifications] = useState([]);
    const [conversations, setConversations] = useState([]);
    const [notificationCount, setNotificationCount] = useState(0);
    const [unreadConversations, setUnreadConversations] = useState({count: 0, ids: []});
    const notificationsRef = useRef(null);
    const messagesRef = useRef(null);
    const navigate = useNavigate();

    useEffect(() =>
    {
        fetchNotifications();
        fetchConversations();
        fetchUnreadConversations();

        let ws;
        if (localStorage.getItem("token"))
        {
            ws = new window.WebSocket(getNotificationWsUrl());
            ws.onmessage = (event) =>
            {
                const msg = JSON.parse(event.data);
                if (msg.type === "new_notification" && msg.data)
                    fetchNotifications();

                if (msg.type === "notifications" && Array.isArray(msg.data))
                {
                    setNotifications(msg.data);
                    setNotificationCount(msg.data.filter(n => !n.is_read).length);
                }
            };
            ws.onerror = (error) =>
            {
                console.error("Websocket error:", error, ws.readyState, ws.url);
            };
        }
        const intervalId = setInterval(() =>
        {
            fetchNotifications();
            fetchConversations();
            fetchUnreadConversations();
        }, 30000);

        return () =>
        {
            clearInterval(intervalId);
            if (ws)
                ws.close();
        };
    }, []);

    useEffect(() =>
    {
        const handleClickOutside = (event) =>
        {
            if (notificationsRef.current && !notificationsRef.current.contains(event.target))
                setShowNotifications(false);

            if (messagesRef.current && !messagesRef.current.contains(event.target))
                setShowMessages(false);
        }

        document.addEventListener("mousedown", handleClickOutside);
        return () => document.removeEventListener("mousedown", handleClickOutside);
    }, []);

    const fetchNotifications = async () =>
    {
        try
        {
            const response = await getAllNotifications();
            if (response.status === "ok" && response.data)
            {
                setNotifications(response.data);
                setNotificationCount(response.data.filter(n => !n.is_read).length);
            }
        }
        catch (error)
        {
            throw error;
        }
    };

    const fetchConversations = async () =>
    {
        try
        {
            const response = await getAllConversations();
            if (response.status === "ok" && response.data)
                setConversations(response.data);
        }
        catch (error)
        {
            throw error;
        }
    };

    const fetchUnreadConversations = async () =>
    {
        try
        {
            const response = await getUnreadConversations();
            if (response.status === "ok" && response.data)
                setUnreadConversations(response.data);
            else
                setUnreadConversations({count: 0, ids: []});
        }
        catch (error)
        {
            setUnreadConversations({count: 0, ids: []});
        }
    };

    const handleNotificationClick = async (notification) =>
    {
        try
        {
            if (!notification.is_read)
            {
                await markNotificationAsRead(notification.id);
                setNotifications(notifications.map(n =>
                    n.id === notification.id ? {...n, is_read: true} : n
                ));
                setNotificationCount(prev => Math.max(0, prev - 1));
            }

            if (notification.type === "follow")
                navigate(`/profile/${notification.actor.id}`);
            else if (notification.type === "like" || notification.type === "comment")
                navigate(`/post/${notification.post_id}`);
            setShowNotifications(false);
        }
        catch (error)
        {
            throw error;
        }
    };

    const handleMessageClick = (conversation) =>
    {
        navigate(`/chat/${conversation.id}`);
        setShowMessages(false);

        if (unreadConversations.ids.includes(conversation.id))
        {
            setUnreadConversations(prev =>
            (
                {
                    count: Math.max(0, prev.count - 1),
                    ids: prev.ids.filter(id => id !== conversation.id)
                }
            )
            );
        }
    };

    const handleLogout = () =>
    {
        localStorage.removeItem("token");
        window.location.href = "/login";
    };

    return (
        <header className="header">
            <div className="header-container">
                <Link to="/" className="header-logo">
                    <img src="/logo.jfif" alt="ITIS Network" />
                    <span>ITIS Network</span>
                </Link>

                <div className="header-right">
                    <div className="header-notifications" ref={notificationsRef}>
                        <button
                            className="notification-button"
                            onClick={() => setShowNotifications(!showNotifications)}
                        >
                            <i className="notification-icon">🔔</i>
                            <span className="notification-label">Notifications</span>
                            {
                                notificationCount > 0 && <span className="notification-badge">{notificationCount}</span>
                            }
                        </button>

                        {
                            showNotifications &&
                            (
                                <div className="dropdown-menu notifications-dropdown">
                                    <h3>Notifications</h3>
                                    {
                                        notifications.length > 0 ?
                                            (
                                                <ul className="notifications-list">
                                                    {
                                                        notifications.map(notification =>
                                                        (
                                                            <li
                                                                key={notification.id}
                                                                className={`notification-item ${!notification.is_read ? "unread" : ""}`}
                                                                onClick={() => handleNotificationClick(notification)}
                                                            >
                                                                {
                                                                    notification.actor &&
                                                                    (
                                                                        <img
                                                                            src={notification.actor.avatar || "/default_avatar.png"}
                                                                            alt={notification.actor.username}
                                                                            className="notification-avatar"
                                                                        />
                                                                    )
                                                                }
                                                                <div className="notification-content">
                                                                    <p>
                                                                        {
                                                                            notification.actor ?
                                                                                (
                                                                                    <strong>{notification.actor.username}</strong>
                                                                                ) :
                                                                                (
                                                                                    "Someone"
                                                                                )
                                                                        }
                                                                        {
                                                                            " "
                                                                        }
                                                                        {
                                                                            notification.type === "follow" && "started following you"
                                                                        }
                                                                        {
                                                                            notification.type === "like" && "liked your post"
                                                                        }
                                                                        {
                                                                            notification.type === "comment" && "commented on your post"
                                                                        }
                                                                    </p>
                                                                    <span className="notification-time">
                                                                        {
                                                                            new Date(notification.created_at).toLocaleDateString()
                                                                        }
                                                                    </span>
                                                                </div>
                                                                {
                                                                    !notification.is_read && <span className="unread-indicator"></span>
                                                                }
                                                            </li>
                                                        )
                                                        )
                                                    }
                                                </ul>
                                            ) :
                                            (
                                                <p className="empty-message">No notifications yet</p>
                                            )
                                    }
                                </div>
                            )
                        }
                    </div>

                    <div className="header-messages" ref={messagesRef}>
                        <button
                            className="message-button"
                            onClick={() => setShowMessages(!showMessages)}
                        >
                            <i className="message-icon">✉️</i>
                            <span className="message-label">Messages</span>
                            {
                                unreadConversations.count > 0 && unreadConversations.ids && unreadConversations.ids.length > 0 && conversations.length > 0 &&
                                (
                                    <span className="notification-badge">{unreadConversations.count}</span>
                                )
                            }
                        </button>

                        {
                            showMessages &&
                            (
                                <div className="dropdown-menu messages-dropdown">
                                    <h3>Messages</h3>
                                    {
                                        conversations.length > 0 ?
                                            (
                                                <ul className="messages-list">
                                                    {
                                                        conversations.map(conversation =>
                                                        (
                                                            <li
                                                                key={conversation.id}
                                                                className={`message-item${unreadConversations.ids.includes(conversation.id) ? " unread" : ""}`}
                                                                onClick={() => handleMessageClick(conversation)}
                                                            >
                                                                <img
                                                                    src={conversation.participants[0].avatar || "/default_avatar.png"}
                                                                    alt={conversation.participants[0].username}
                                                                    className="message-avatar"
                                                                />
                                                                <div className="message-content">
                                                                    <p className="message-username">{conversation.participants[0].username}</p>
                                                                    <span className="message-time">
                                                                        {
                                                                            new Date(conversation.created_at).toLocaleDateString()
                                                                        }
                                                                    </span>
                                                                </div>
                                                                {
                                                                    unreadConversations.ids.includes(conversation.id) && <span className="unread-indicator"></span>
                                                                }
                                                            </li>
                                                        )
                                                        )
                                                    }
                                                </ul>
                                            ) :
                                            (
                                                <p className="empty-message">No conversations yet</p>
                                            )
                                    }
                                    <Link to="/chat" className="view-all-link">View all messages</Link>
                                </div>
                            )
                        }
                    </div>

                    <button onClick={handleLogout} className="logout-button">
                        Logout
                    </button>
                </div>
            </div>
        </header>
    );
}

export default Header;
