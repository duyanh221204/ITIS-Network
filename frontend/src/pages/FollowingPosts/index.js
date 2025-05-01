import { useState, useEffect } from 'react';
import { getFollowingPosts } from '../../services/postService';
import Post from '../../components/Post';
import CreatePostForm from '../../components/CreatePostForm';
import './styles.css';

const FollowingPosts = () =>
{
    const [posts, setPosts] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    useEffect(() =>
    {
        fetchPosts();
    }, []);

    const fetchPosts = async () =>
    {
        setLoading(true);
        try
        {
            const response = await getFollowingPosts();
            if (response.status === 'ok')
                setPosts(response.data || []);
            else
                setError('Failed to fetch posts');
        }
        catch (err)
        {
            setError('Error loading posts');
            console.error(err);
        }
        finally
        {
            setLoading(false);
        }
    };

    const handlePostCreated = () =>
    {
        fetchPosts();
    };

    return (
        <div className="following-posts-page">
            <h1 className="page-title">Following Posts</h1>

            <CreatePostForm onPostCreated={handlePostCreated} />

            {loading ? (
                <div className="loading">
                    <div className="loading-spinner"></div>
                </div>
            ) : error ? (
                <div className="error-container">
                    <p className="error-message">{error}</p>
                    <button onClick={fetchPosts} className="btn btn-primary">
                        Try Again
                    </button>
                </div>
            ) : (
                <>
                    {posts.length > 0 ? (
                        <div className="posts-container">
                            {posts.map(post => (
                                <Post key={post.id} post={post} refreshPosts={fetchPosts} />
                            ))}
                        </div>
                    ) : (
                        <div className="empty-posts">
                            <p>No posts from people you follow. Follow other users to see their posts here!</p>
                        </div>
                    )}
                </>
            )}
        </div>
    );
}

export default FollowingPosts;
