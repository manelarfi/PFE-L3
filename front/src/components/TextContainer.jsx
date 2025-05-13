import React, { useState } from 'react';

const TextInputContainer = () => {
const [userText, setUserText] = useState('');

  const handleChange = (e) => {
    setUserText(e.target.value);
  };
  
  //const handleSubmit = () => {
    //alert(`You typed: ${userText}`);
    // Here userText is the text entered by the user
    //  send userText to the backend 
//  };

  return (
    <div style={{ padding: '20px', maxWidth: '400px' }}>
      <textarea className='text-input'
        value={userText}
        onChange={handleChange}
        placeholder="Type your message here..."
       
      />

      <button className='submit-button'> Submit </button>

    </div>
  );
};

export default TextInputContainer;
