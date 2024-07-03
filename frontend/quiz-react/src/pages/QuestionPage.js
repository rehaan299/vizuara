import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

function QuestionPage() {
    const [question, setQuestion] = useState(null);
    const [answer, setAnswer] = useState('');
    const [error, setError] = useState('');
    const navigate = useNavigate();

    useEffect(() => {
        axios.post('http://127.0.0.1:5000/api/start')
            .then(response => {
                setQuestion(response.data.questions[0]);
                console.log('Initial question:', response.data.questions[0]);
            })
            .catch(error => {
                console.error('There was an error starting the quiz!', error);
                setError('There was an error starting the quiz.');
            });
    }, []);

    const handleSubmit = (e) => {
        e.preventDefault();
        console.log('Submitting answer:', answer);
        axios.post('http://127.0.0.1:5000/api/question', { answer: answer })
            .then(response => {
                console.log('Response:', response.data);
                if (response.data.proficiency !== undefined) {
                    navigate('/results');
                } else {
                    setQuestion(response.data.question);
                    setAnswer('');
                }
            })
            .catch(error => {
                console.error('There was an error submitting the answer!', error);
                setError('There was an error submitting the answer.');
            });
    };

    if (!question) {
        return <div>Loading...</div>;
    }

    return (
        <div>
            <h2>Question</h2>
            <p>{question.Question}</p>
            <form onSubmit={handleSubmit}>
                {question.Options.map((option, index) => (
                    <div key={index}>
                        <input
                            type="radio"
                            id={`option${index}`}
                            name="answer"
                            value={index + 1}
                            onChange={(e) => setAnswer(e.target.value)}
                        />
                        <label htmlFor={`option${index}`}>{option}</label>
                    </div>
                ))}
                <button type="submit">Submit</button>
            </form>
            {error && <p style={{ color: 'red' }}>{error}</p>}
        </div>
    );
}

export default QuestionPage;
