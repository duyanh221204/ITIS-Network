import { useState, useEffect } from 'react';
import { getNotFollowedUsers, followUser } from '../../services/profileService';
import UserList from '../../components/UserList';
import './styles.css';

const Discover = () =>
{
    const [users, setUsers] = useState([]);
    const [filteredUsers, setFilteredUsers] = useState([]);
    const [loading, setLoading] = useState(true);
    const [searchTerm, setSearchTerm] = useState('');
    const [error, setError] = useState('');

    useEffect(() =>
    {
        fetchUsers();
    }, []);

    useEffect(() =>
    {
        if (searchTerm.trim())
        {
            const filtered = users.filter(user =>
                user.username.toLowerCase().includes(searchTerm.toLowerCase())
            );
            setFilteredUsers(filtered);
        }
        else
            setFilteredUsers(users);
    }, [searchTerm, users]);

    const fetchUsers = async () =>
    {
        setLoading(true);
        try
        {
            const response = await getNotFollowedUsers();
            if (response.status === 'ok')
            {
                setUsers(response.data || []);
                setFilteredUsers(response.data || []);
            }
            else
            {
                setError('Failed to fetch users');
            }
        }
        catch (err)
        {
            setError('Error loading users');
            console.error(err);
        }
        finally
        {
            setLoading(false);
        }
    };

    const handleFollow = async (userId) =>
    {
        try
        {
            const response = await followUser(userId);
            if (response.status === 'ok')
            {
                const updatedUsers = users.filter(user => user.id !== userId);
                setUsers(updatedUsers);
                setFilteredUsers(filteredUsers.filter(user => user.id !== userId));
            }
        }
        catch (error)
        {
            console.error('Error following user:', error);
        }
    };

    return (
        <div className="discover-page">
            <h1 className="page-title">Discover People</h1>

            <div className="search-container">
                <input
                    type="text"
                    className="search-input"
                    placeholder="Search by username..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                />
            </div>

            {loading ? (
                <div className="loading">
                    <div className="loading-spinner"></div>
                </div>
            ) : error ? (
                <div className="error-container">
                    <p className="error-message">{error}</p>
                    <button onClick={fetchUsers} className="btn btn-primary">
                        Try Again
                    </button>
                </div>
            ) : (
                <div className="users-container">
                    <UserList
                        users={filteredUsers}
                        emptyMessage={
                            searchTerm ?
                                "No users match your search" :
                                "No more users to discover. You've followed everyone!"
                        }
                        onFollowAction={handleFollow}
                    />
                </div>
            )}
        </div>
    );
}

export default Discover;
