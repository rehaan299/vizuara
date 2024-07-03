import React, { useState } from 'react';
import { Button } from './styles';

const Question = ({ question, handleAnswer }) => {
  const [selectedOption, setSelectedOption] = useState(null);

  const onSubmit = (event) => {
    event.preventDefault();
    handleAnswer(selectedOption);
  };

  return (
    <div>
      <h2>{question.Question}</h2>
      <form onSubmit={onSubmit}>
        {question.Options.map((option, index) => (
          <div key={index}>
            <input
              type="radio"
              id={`option${index}`}
              name="option"
              value={index}
              onChange={(e) => setSelectedOption(e.target.value)}
            />
            <label htmlFor={`option${index}`}>{option}</label>
          </div>
        ))}
        <Button type="submit">Submit</Button>
      </form>
    </div>
  );
};

export default Question;
