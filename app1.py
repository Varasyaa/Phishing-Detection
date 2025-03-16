import React, { useState } from 'react';
import axios from 'axios';

function App() {
    const [emailContent, setEmailContent] = useState('');
    const [result, setResult] = useState(null);

    const handleInputChange = (event) => {
        setEmailContent(event.target.value);
    };

    const handleDetectPhishing = async () => {
        if (!emailContent.trim()) return;
        try {
            const response = await axios.post('http://127.0.0.1:5000/detect_phishing', {
                email_content: emailContent,
            });
            setResult(response.data);
        } catch (error) {
            console.error('Error detecting phishing:', error);
        }
    };

    return (
        <div className="min-h-screen flex flex-col items-center justify-center bg-gray-100 p-6">
            <h1 className="text-3xl font-bold mb-4">AI-Based Phishing Email Detection</h1>
            <textarea
                className="w-full max-w-lg p-2 border rounded"
                rows="6"
                placeholder="Paste email content here..."
                value={emailContent}
                onChange={handleInputChange}
            ></textarea>
            <button onClick={handleDetectPhishing} className="bg-blue-500 text-white px-4 py-2 mt-4 rounded">
                Detect Phishing
            </button>
            {result && (
                <div className="mt-4 p-4 bg-white shadow-md rounded">
                    <p><strong>Prediction:</strong> {result.prediction}</p>
                </div>
            )}
        </div>
    );
}

export default App;
