import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Quiz from '../components/Quiz';
import Results from './ResultsPage';
import { Container } from '../components/styles';

const QuizPage = () => {
  const [questions, setQuestions] = useState([]);
  const [currentQuestion, setCurrentQuestion] = useState(null);
  const [proficiency, setProficiency] = useState(null);
  const [quizFinished, setQuizFinished] = useState(false);

  useEffect(() => {
    console.log('Starting quiz...');
    axios.post('http://127.0.0.1:5000/api/start')
      .then(response => {
        console.log('Quiz started:', response.data.questions);
        setQuestions(response.data.questions);
        setCurrentQuestion(0);
      })
      .catch(error => {
        console.error('There was an error starting the quiz!', error);
      });
  }, []);

  const handleAnswer = (answer) => {
    const data = { answer: answer };
    axios.post('http://127.0.0.1:5000/api/question', data)
      .then(response => {
        if (response.data.proficiency !== undefined) {
          console.log('Received proficiency:', response.data.proficiency);
          setProficiency(response.data.proficiency);
          getNextQuestion(response.data.proficiency);
        } else {
          setCurrentQuestion(currentQuestion + 1);
        }
      })
      .catch(error => {
        console.error('There was an error submitting the answer!', error);
      });
  };

  const getNextQuestion = (currentProficiency) => {
    const data = { answer: currentProficiency };
    axios.post('http://127.0.0.1:5000/api/next_question', data)
      .then(response => {
        console.log('Next question:', response.data.question);
        setQuestions([...questions, response.data.question]);
        setCurrentQuestion(questions.length);
      })
      .catch(error => {
        console.error('There was an error fetching the next question!', error);
      });
  };

  const finishQuiz = () => {
    setQuizFinished(true);
  };

  if (quizFinished) {
    return <Results />;
  }

  if (questions.length === 0 || currentQuestion === null) {
    return <div>Loading...</div>;
  }

  if (currentQuestion >= questions.length) {
    return <div>Quiz complete! Proficiency: {proficiency}</div>;
  }

  return (
    <Container>
      <h1>Quiz Application</h1>
      <Quiz question={questions[currentQuestion]} handleAnswer={handleAnswer} />
      {currentQuestion >= questions.length && <button onClick={finishQuiz}>Finish Quiz</button>}
    </Container>
  );
};

export default QuizPage;
