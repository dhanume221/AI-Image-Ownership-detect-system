import { Link } from 'react-router-dom';

const Navbar = () => {
    return (
        <nav style={{
            display: 'flex',
            justifyContent: 'space-between',
            padding: '1rem',
            background: 'var(--card-bg)',
            borderBottom: '1px solid var(--border-color)',
            marginBottom: '2rem'
        }}>
            <div style={{ fontSize: '1.5rem', fontWeight: 'bold' }}>
                <Link to="/" style={{ textDecoration: 'none', color: 'var(--primary-color)' }}>AI Ownership Registry</Link>
            </div>
            <div>
                <Link to="/" style={{ margin: '0 1rem', textDecoration: 'none', color: 'var(--text-color)' }}>Register</Link>
                <Link to="/verify" style={{ margin: '0 1rem', textDecoration: 'none', color: 'var(--text-color)' }}>Verify</Link>
            </div>
        </nav>
    );
};

export default Navbar;
