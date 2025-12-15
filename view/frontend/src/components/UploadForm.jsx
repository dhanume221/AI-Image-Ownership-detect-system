import { useState } from 'react';
import api from '../api';

const UploadForm = ({ endpoint, title, onSuccess }) => {
    const [file, setFile] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const handleFileChange = (e) => {
        setFile(e.target.files[0]);
        setError(null);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!file) {
            setError("Please select a file.");
            return;
        }
        setLoading(true);
        const formData = new FormData();
        formData.append('file', file);
        // Add dummy fields if registering (owner usually comes from auth, but we might likely need it if we didn't implement auth token on frontend yet)

        try {
            const response = await api.post(endpoint, formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });
            onSuccess(response.data);
            setFile(null); // Reset file input
        } catch (err) {
            console.error(err);
            setError(err.response?.data?.error || "An error occurred");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="card">
            <h2>{title}</h2>
            <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '1rem', alignItems: 'center' }}>
                <input type="file" onChange={handleFileChange} accept="image/*" />
                {error && <div style={{ color: 'var(--danger-color)' }}>{error}</div>}
                <button type="submit" disabled={loading}>
                    {loading ? 'Processing...' : 'Upload'}
                </button>
            </form>
        </div>
    );
};

export default UploadForm;
