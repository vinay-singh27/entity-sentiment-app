// frontend/src/index.js
import React from 'react';
import ReactDOM from 'react-dom';
import App from './components/App';
import './index.css';  // You can create a custom CSS file for index styling
import * as serviceWorker from './serviceWorker.js';

ReactDOM.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
  document.getElementById('root')
);

serviceWorker.unregister(); // Change to .register() for enabling service worker
