// frontend/src/components/EntityCard.js
import React from 'react';

function EntityCard({ entity }) {
  return (
    <div className="entity-card">
      <h3>{entity.text}</h3>
      <p>Sentiment: {entity.sentiment}</p>
    </div>
  );
}

export default EntityCard;
