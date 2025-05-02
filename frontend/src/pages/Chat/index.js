import {useState, useEffect, useRef} from "react";
import {useNavigate, useParams} from "react-router-dom";
import {getAllConversations, getAllMessages, sendMessage, markConversationAsRead, getWebSocketUrl} from "../../services/chatService";
import "./styles.css";

const Chat = () =>
{
    const { conversationId } = useParams();
    const navigate = useNavigate();
    const [conversations, setConversations] = useState([]);
    const [messages, setMessages] = useState([]);
    const [newMessage, setNewMessage] = useState("");
    const [loading, setLoading] = useState(true);
    const [sendingMessage, setSendingMessage] = useState(false);
    const [error, setError] = useState("");
    const messagesEndRef = useRef(null);
    const wsRef = useRef(null);
    const currentUserId = parseInt(localStorage.getItem("userId"));

    useEffect(() =>
    {
        fetchConversations();

        return () =>
        {
            if (wsRef.current)
                wsRef.current.close();
        };
    }, []);

    useEffect(() =>
    {
        if (conversationId)
        {
            fetchMessages().then(() =>
            {
                setTimeout(scrollToBottom, 0);
            });
            setupWebSocket();
            setNewMessage("");
        }
        else
            setMessages([]);
    }, [conversationId]);

    useEffect(() =>
    {
        scrollToBottom();
    }, [messages]);

    const setupWebSocket = () =>
    {
        if (wsRef.current)
            wsRef.current.close();

        const wsUrl = getWebSocketUrl(conversationId);
        const ws = new WebSocket(wsUrl);

        ws.onopen = () =>
        {
            console.log("WebSocket connection established");
        };

        ws.onmessage = (event) =>
        {
            const data = JSON.parse(event.data);
            setMessages(prev =>
            {
                if (prev.some(m => m.id === data.id))
                    return prev;
                return [
                    ...prev,
                    {
                        id: data.id,
                        content: data.content,
                        created_at: data.created_at,
                        sender: { id: data.sender_id },
                        is_read: false
                    }
                ];
            });
        };

        ws.onerror = (error) =>
        {
            throw error;
        };

        ws.onclose = () =>
        {
            console.log("WebSocket connection closed");
        };

        wsRef.current = ws;
    };

    const fetchConversations = async () =>
    {
        setLoading(true);
        try
        {
            const response = await getAllConversations();
            if (response.status === "ok")
                setConversations(response.data || []);
        }
        catch (error)
        {
            throw error;
        }
        finally
        {
            setLoading(false);
        }
    };

    const fetchMessages = async () =>
    {
        if (!conversationId)
            return;

        setLoading(true);
        try
        {
            const messagesResponse = await getAllMessages(conversationId);
            if (messagesResponse.status === "ok")
                setMessages(messagesResponse.data || []);

            await markConversationAsRead(conversationId);

            setConversations
            (prevConversations =>
                prevConversations.map(conv =>
                    conv.id === parseInt(conversationId) ? {...conv, hasUnread: false} : conv
                )
            );
        }
        catch (error)
        {
            setError("Failed to load messages");
            throw error;
        }
        finally
        {
            setLoading(false);
        }
    };

    const handleSendMessage = async (e) =>
    {
        e.preventDefault();

        if (!newMessage.trim() || !conversationId || sendingMessage)
            return;

        setSendingMessage(true);
        try
        {
            const tempId = "pending-" + Date.now();
            const tempMsg =
                {
                    id: tempId,
                    content: newMessage,
                    created_at: new Date().toISOString(),
                    sender:
                        {
                            id: currentUserId
                        },
                    is_read: false
                };
            setMessages(prev => [...prev, tempMsg]);
            setNewMessage("");
            setTimeout(scrollToBottom, 0);

            const res = await sendMessage(conversationId, tempMsg.content);
            if (res && res.data)
            {
                setMessages(prev =>
                    [
                        ...prev.filter(m => m.id !== tempId),
                        {
                            id: res.data.id,
                            content: res.data.content,
                            created_at: res.data.created_at,
                            sender:
                                {
                                    id: currentUserId
                                },
                            is_read: false
                        }
                    ]
                );
            }
        }
        catch (error)
        {
            setMessages(prev => prev.filter(m => !("id" in m && String(m.id).startsWith("pending-"))));
            throw error;
        }
        finally
        {
            setSendingMessage(false);
        }
    };

    const scrollToBottom = () =>
    {
        messagesEndRef.current?.scrollIntoView({behavior: "smooth"});
    };

    const selectConversation = (convId) =>
    {
        navigate(`/chat/${ convId }`);
    };

    const currentConversation = conversations.find(conv => conv.id === parseInt(conversationId));

    return (
        <div className="chat-page">
            <div className="chat-container">
                <div className="conversations-sidebar">
                    <h2 className="sidebar-title">Conversations</h2>

                    {
                        loading && !conversationId && conversations.length === 0 ?
                            (
                                <div className="loading sidebar-loading">
                                    <div className="loading-spinner"></div>
                                </div>
                            ) :
                            conversations.length > 0 ?
                                (
                                    <ul className="conversations-list">
                                        {
                                            conversations.map(conversation =>
                                                (
                                                    <li
                                                        key={conversation.id}
                                                        className={`conversation-item ${parseInt(conversationId) === conversation.id ? "active" : ""}`}
                                                        onClick={() => selectConversation(conversation.id)}
                                                    >
                                                        <img
                                                            src={conversation.participants[0].avatar || "/default_avatar.png" }
                                                            alt={conversation.participants[0].username}
                                                            className="conversation-avatar"
                                                        />
                                                        <div className="conversation-info">
                                                            <span className="conversation-name">
                                                                {
                                                                    conversation.participants[0].username
                                                                }
                                                            </span>
                                                            <span className="conversation-time">
                                                                {
                                                                    new Date(conversation.created_at).toLocaleDateString()
                                                                }
                                                            </span>
                                                        </div>
                                                        {
                                                            conversation.hasUnread && <span className="unread-indicator"></span>
                                                        }
                                                    </li>
                                                )
                                            )
                                        }
                                    </ul>
                                ) :
                                (
                                    <p className="empty-state">No conversations yet.</p>
                                )
                    }
                </div>

                <div className="messages-container">
                    {
                        conversationId ?
                            (
                                <>
                                    <div className="messages-header">
                                        {
                                            currentConversation &&
                                            (
                                                <>
                                                    <img
                                                        src={currentConversation.participants[0].avatar || "/default_avatar.png"}
                                                        alt={currentConversation.participants[0].username}
                                                        className="header-avatar"
                                                    />
                                                    <span className="header-name">
                                                        {
                                                            currentConversation.participants[0].username
                                                        }
                                                    </span>
                                                </>
                                            )
                                        }
                                    </div>

                                    <div className="messages-list">
                                        {
                                            loading ?
                                                (
                                                    <div className="loading">
                                                        <div className="loading-spinner"></div>
                                                    </div>
                                                ) :
                                                error ?
                                                    (
                                                        <div className="error-container">
                                                            <p className="error-message">{error}</p>
                                                            <button onClick={fetchMessages} className="btn btn-primary">
                                                                Try Again
                                                            </button>
                                                        </div>
                                                    ) :
                                                    messages.length > 0 ?
                                                        (
                                                            <>
                                                                {
                                                                    messages.map(message =>
                                                                        (
                                                                            <div
                                                                                key={message.id}
                                                                                className={`message ${message.sender.id === currentUserId ? "my-message" : "other-message"}`}
                                                                            >
                                                                                <div className="message-content">{message.content}</div>
                                                                                <div className="message-info">
                                                                                    <span className="message-time">
                                                                                        {
                                                                                            new Date(message.created_at).toLocaleTimeString([], {hour: "2-digit", minute: "2-digit"})
                                                                                        }
                                                                                    </span>
                                                                                    {
                                                                                        message.sender.id === currentUserId &&
                                                                                        (
                                                                                            <span className={`read-status ${message.is_read ? "read" : ""}`}>
                                                                                                {
                                                                                                    message.is_read ? "✓✓" : "✓"
                                                                                                }
                                                                                            </span>
                                                                                        )
                                                                                    }
                                                                                </div>
                                                                            </div>
                                                                        )
                                                                    )
                                                                }
                                                                <div ref={messagesEndRef} />
                                                            </>
                                                        ) :
                                                        (
                                                            <div className="empty-state">
                                                                Start a conversation by sending a message.
                                                            </div>
                                                        )
                                        }
                                    </div>

                                    <form className="message-form" onSubmit={handleSendMessage}>
                                        <input
                                            type="text"
                                            className="message-input"
                                            placeholder="Type a message..."
                                            value={newMessage}
                                            onChange={(e) => setNewMessage(e.target.value)}
                                        />
                                        <button
                                            type="submit"
                                            className="send-button"
                                            disabled={!newMessage.trim() || sendingMessage}
                                        >
                                            {
                                                sendingMessage ? "..." : "Send"
                                            }
                                        </button>
                                    </form>
                                </>
                            ) :
                            (
                                <div className="empty-state select-conversation">
                                    Select a conversation to start chatting
                                </div>
                            )
                    }
                </div>
            </div>
        </div>
    );
}

export default Chat;
