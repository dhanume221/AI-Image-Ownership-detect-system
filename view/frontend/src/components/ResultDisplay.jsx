const ResultDisplay = ({ result }) => {
    if (!result) return null;

    return (
        <div className="card" style={{ marginTop: '2rem', textAlign: 'left' }}>
            <h3>Result</h3>
            <pre style={{ background: '#0d1117', padding: '1rem', borderRadius: '8px', overflowX: 'auto' }}>
                {JSON.stringify(result, null, 2)}
            </pre>
            {result.status === 'exact_match' && (
                <div style={{ color: 'var(--primary-color)', marginTop: '1rem' }}>
                    <strong>Confirmed Owner:</strong> {result.owner}
                </div>
            )}
            {result.status === 'similar_match' && (
                <div style={{ color: 'orange', marginTop: '1rem' }}>
                    <strong>Potential Match Found:</strong> {result.owner} (Score: {result.score})
                </div>
            )}
        </div>
    );
};

export default ResultDisplay;
