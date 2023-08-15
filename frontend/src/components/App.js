// frontend/src/components/App.js
import React, { useState } from 'react';
import '../css/App.css';
import EntityCard from './EntityCard';
import axios from 'axios';

function App() {
  const [inputText, setInputText] = useState('');
  const [result, setResult] = useState(null);
  const [isSentimentAnalysis, setIsSentimentAnalysis] = useState(true);

  const analyzeText = async () => {
    try {
      const response = await axios.post('/api/analyze', { text: inputText });
      setResult(response.data);
    } catch (error) {
      console.error('Error analyzing text:', error);
    }
  };

  const toggleAnalysisMode = () => {
    setIsSentimentAnalysis(!isSentimentAnalysis);
    setResult(null);
  };

  return (
    <div className="App">
      <header>
        <h1>Entity Sentiment Analysis</h1>
      </header>
      <main>
        <div className="input-container">
          <textarea
            placeholder="Enter your text here..."
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
          />
          <button onClick={analyzeText}>Run Analysis</button>
          <label className="option">
            <input
              type="checkbox"
              checked={!isSentimentAnalysis}
              onChange={toggleAnalysisMode}
            />
            OpenAI
          </label>
        </div>

        {result && (
          <div className="output-container">
            <h2>{isSentimentAnalysis ? 'Sentiment' : 'Entities'}</h2>
            {isSentimentAnalysis ? (
              <p>Sentiment: {result.sentiment}</p>
            ) : (
              <div className="entity-list">
                {result.entities.map((entity, index) => (
                  <EntityCard key={index} entity={entity} />
                ))}
              </div>
            )}
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
