import { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import UploadForm from './components/UploadForm';
import ResultDisplay from './components/ResultDisplay';

function App() {
  const [result, setResult] = useState(null);

  return (
    <Router>
      <Navbar />
      <div className="container">
        <Routes>
          <Route path="/" element={
            <div>
              <h1>Register Content</h1>
              <p style={{ marginBottom: '2rem', color: '#8b949e' }}>
                Upload your creative work to register ownership on the blockchain-backed registry.
              </p>
              <UploadForm
                endpoint="register/"
                title="Upload New Content"
                onSuccess={(data) => setResult({ ...data, status: 'Registered Successfully' })}
              />
              {result && <ResultDisplay result={result} />}
            </div>
          } />
          <Route path="/verify" element={
            <div>
              <h1>Verify Ownership</h1>
              <p style={{ marginBottom: '2rem', color: '#8b949e' }}>
                Upload content to check against the registry for ownership or similarity.
              </p>
              <UploadForm
                endpoint="verify/"
                title="Check Content"
                onSuccess={(data) => setResult(data)}
              />
              {result && <ResultDisplay result={result} />}
            </div>
          } />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
