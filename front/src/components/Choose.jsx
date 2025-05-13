import React, { useState } from 'react';

function Chooser() {
  const [selectedOption, setSelectedOption] = useState('');

  const handleChange = (e) => {
    const value = e.target.value;
    setSelectedOption(value);

    // Execute code based on selection
    if (value === 'option1') {
      console.log("You chose Option 1");
      // Do something for option 1
    } else if (value === 'option2') {
      console.log("You chose Option 2");
      // Do something for option 2
    } else if (value === 'option3') {
      console.log("You chose Option 3");
      // Do something for option 3
    }
  };

  return (
    <div className="chooser">
      <label htmlFor="selector">Choose an option: </label>
      <select id="selector" onChange={handleChange}>
        <option value="">-- Select --</option>
        <option value="option1">Option 1</option>
        <option value="option2">Option 2</option>
        <option value="option3">Option 3</option>
      </select>
    </div>
  );
}


export default Chooser;
