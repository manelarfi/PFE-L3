import React, { useState } from 'react';

const TextInputContainer = () => {
  const [userText, setUserText] = useState('');

  const handleChange = (e) => {
    setUserText(e.target.value);
  };
  
  const handleSubmit = () => {
    alert(`You typed: ${userText}`);
    // You can also send userText to a backend or use it anywhere
    
  };

  return (
    <div style={{ padding: '20px', maxWidth: '400px' }}>
      <textarea className='text-input'
        value={userText}
        onChange={handleChange}
        placeholder="Type your message here..."
       
      />

      <button className='submit-button'
        onClick={handleSubmit}
       
      >
        Submit
      </button>

    </div>
  );
};

export default TextInputContainer;
