import React, { useEffect, useState } from 'react';
import axios from 'axios';

function ResultsPage() {
  const [results, setResults] = useState(null);

  useEffect(() => {
    axios.get('http://127.0.0.1:5000/api/results')
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
      <h2>Quiz Results</h2>
      <p>Score: {results.score}</p>
      <p>Total Questions: {results.total}</p>
      <p>Accuracy: {results.accuracy}%</p>
      <p>Proficiency: {results.proficiency}%</p>
    </div>
  );
}

export default ResultsPage;
