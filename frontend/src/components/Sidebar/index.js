import { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import './styles.css';

const Sidebar = () =>
{
    const location = useLocation();
    const [isOpen, setIsOpen] = useState(true);

    const toggleSidebar = () =>
    {
        setIsOpen(!isOpen);
    };

    const isActive = (path) =>
    {
        return location.pathname === path;
    };

    return (
        <>
            <div className={ `sidebar-toggle ${ isOpen ? 'open' : 'closed' }` } onClick={ toggleSidebar }>
                { isOpen ? '←' : '→' }
            </div>
            <aside className={ `sidebar ${ isOpen ? 'open' : 'closed' }` }>
                <div className="sidebar-content">
                    <nav className="sidebar-nav">
                        <ul>
                            <li className={ isActive('/') ? 'active' : '' }>
                                <Link to="/">
                                    <i className="sidebar-icon">🏠</i>
                                    <span>Newsfeed</span>
                                </Link>
                            </li>
                            <li className={ isActive('/following-posts') ? 'active' : '' }>
                                <Link to="/following-posts">
                                    <i className="sidebar-icon">👥</i>
                                    <span>Following Posts</span>
                                </Link>
                            </li>
                            <li className={ isActive('/discover') ? 'active' : '' }>
                                <Link to="/discover">
                                    <i className="sidebar-icon">🔍</i>
                                    <span>Discover People</span>
                                </Link>
                            </li>
                            <li className={ isActive('/create-post') ? 'active' : '' }>
                                <Link to="/create-post">
                                    <i className="sidebar-icon">✏️</i>
                                    <span>Create Post</span>
                                </Link>
                            </li>
                            <li className={ isActive('/profile/me') ? 'active' : '' }>
                                <Link to="/profile/me">
                                    <i className="sidebar-icon">👤</i>
                                    <span>My Profile</span>
                                </Link>
                            </li>
                            <li className={ isActive('/settings') ? 'active' : '' }>
                                <Link to="/settings">
                                    <i className="sidebar-icon">⚙️</i>
                                    <span>Settings</span>
                                </Link>
                            </li>
                        </ul>
                    </nav>
                </div>
            </aside>
        </>
    );
}

export default Sidebar;
