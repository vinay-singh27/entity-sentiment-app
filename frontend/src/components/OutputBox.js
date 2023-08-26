import React from 'react';
import './OutputBox.css'; // Styles

const OutputBox = ({ outputText }) => {
  return <div className="output-box">{outputText}</div>;
};

export default OutputBox;
