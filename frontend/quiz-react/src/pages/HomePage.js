import React from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

function HomePage() {
  const navigate = useNavigate();

  const startQuiz = () => {
    axios.post('http://127.0.0.1:5000/api/start')
      .then(response => {
        console.log('Quiz started:', response.data);
        navigate('/question');
      })
      .catch(error => {
        console.error('There was an error starting the quiz!', error);
      });
  };

  return (
    <div>
      <h1>Welcome to the Quiz</h1>
      <button onClick={startQuiz}>Start Quiz</button>
    </div>
  );
}

export default HomePage;
