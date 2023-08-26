import React, { useState } from 'react';
import './Button.css'; // Styles

const Button = ({ label }) => {
  const [inputText, setInputText] = useState('');
  const [outputText, setOutputText] = useState('');

  const handleClick = async () => {
    try {
      const response = await fetch('/capitalize', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ inputText })
      });

      if (response.ok) {
        const data = await response.json();
        setOutputText(data.capitalizedText);
      } else {
        console.error('Error while fetching data');
      }
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <div >
      <div className="input-container">
      <textarea className="text-input" type="text" placeholder="Enter text here.."  value={inputText}
        onChange={(e) => setInputText(e.target.value)}
      />
      </div>
      <button className="run-button" onClick={handleClick}>
        {label}
      </button>
      <div className="output-box">{outputText}</div>
    </div>
  );
};

export default Button;
