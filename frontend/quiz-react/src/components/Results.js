import React, { useEffect, useState } from 'react';
import axios from 'axios';

function Results() {
  const [results, setResults] = useState(null);

  useEffect(() => {
    axios.get('http://localhost:5000/api/results')
      .then(response => {
        setResults(response.data);
      })
      .catch(error => {
        console.error('There was an error fetching the results!', error);
      });
  }, []);

  if (!results) {
    return <div>Loading...</div>;
  }

  return (
    <div>
      <h1>Quiz Results</h1>
      <p>Score: {results.score} / {results.total}</p>
      <p>Accuracy: {results.accuracy}%</p>
      <p>Proficiency: {results.proficiency}%</p>
      <button onClick={() => window.location.reload()}>Restart Quiz</button>
    </div>
  );
}

export default Results;
