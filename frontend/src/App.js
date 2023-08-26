import React, {useState, useEffect} from 'react';
import './App.css'; // Styles
import Header from './components/Header';
import Button from './components/Button';
import OutputBox from './components/OutputBox';

function App() {
  const handleRunAnalysis = () => {
    // Logic for analysis and updating output
  };

  return (
    <div className="app">
      <div className='Inner'> 
      <Header />
      <div className="content">
        <Button label="Run Analysis" onClick={handleRunAnalysis} />
      </div>
      </div>
    </div>
  );
}

export default App;
