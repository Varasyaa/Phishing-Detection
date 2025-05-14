import React, { useState } from 'react';
import axios from 'axios';

function PhishingCheck() {
  const [url, setUrl] = useState('');
  const [result, setResult] = useState(null);

  const checkUrl = async () => {
    const res = await axios.post('http://localhost:5000/predict', { url });
    setResult(res.data.phishing ? "⚠️ Phishing Detected" : "✅ Safe");
  };

  return (
    <div className="p-4 max-w-md mx-auto">
      <h2 className="text-xl font-bold mb-4">Phishing URL Detector</h2>
      <input
        value={url}
        onChange={(e) => setUrl(e.target.value)}
        placeholder="Enter a URL"
        className="border p-2 w-full"
      />
      <button onClick={checkUrl} className="bg-blue-600 text-white px-4 py-2 mt-2">Check</button>
      {result && <div className="mt-4">{result}</div>}
    </div>
  );
}

export default PhishingCheck;
