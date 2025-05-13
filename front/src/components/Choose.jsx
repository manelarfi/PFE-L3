import React, { useState } from 'react';

function Chooser() {
  const [selectedOption, setSelectedOption] = useState('');

  const handleChange = (e) => {
    const value = e.target.value;
    setSelectedOption(value);

    // Execute code based on selection
    if (value === 'LSB') {
      console.log("You chose Option 1");
      // Do something for option 1
    } else if (value === 'DCT') {
      console.log("You chose Option 2");
      // Do something for option 2
    } else if (value === 'DWT') {
      console.log("You chose Option 3");
      // Do something for option 3
    }
  };

  return (
    <div className="chooser">
      <label htmlFor="selector">Choose an option: </label>
      <select id="selector" onChange={handleChange}>
        <option value="">-- Select --</option>
        <option value="LSB">LSB</option>
        <option value="DCT">DCT</option>
        <option value="DWT">DWT</option>
      </select>
    </div>
  );
}


export default Chooser;
