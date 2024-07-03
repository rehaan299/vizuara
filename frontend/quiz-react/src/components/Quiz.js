import React, { useState } from 'react';

const Quiz = ({ question, handleAnswer }) => {
  const [selectedAnswer, setSelectedAnswer] = useState(null);

  const onAnswerChange = (e) => {
    setSelectedAnswer(e.target.value);
  };

  const onSubmit = () => {
    if (selectedAnswer !== null) {
      handleAnswer(selectedAnswer);
    } else {
      alert('Please select an answer before submitting.');
    }
  };

  return (
    <div>
      <h2>{question.Question}</h2>
      <ul>
        {question.Options.map((option, index) => (
          <li key={index}>
            <label>
              <input
                type="radio"
                name="answer"
                value={index + 1}
                onChange={onAnswerChange}
              />
              {option}
            </label>
          </li>
        ))}
      </ul>
      <button onClick={onSubmit}>Submit</button>
    </div>
  );
};

export default Quiz;
