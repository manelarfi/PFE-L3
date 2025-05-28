import React, { useState } from 'react';


// This component allows the user to choose a method TO HIDE the data 
function Chooser() {
  const [selectedOption, setSelectedOption] = useState('');

  const handleChange = (e) => {
    const value = e.target.value;
    setSelectedOption(value);

    // Execute code based on selection
    if (value === 'LSBhide') {
      console.log("You chose Option 1");
      // Do something for option 1
    } else if (value === 'DCThide') {
      console.log("You chose Option 2");
      // Do something for option 2
    } else if (value === 'DWThide') {
      console.log("You chose Option 3");
      // Do something for option 3
    }
  };

  return (
    <div className="chooser">
      <label htmlFor="selector">Choose your method: </label>
      <select id="selector" onChange={handleChange}>
        <option value="">-- Select --</option>
        <option value="LSBhide">LSB</option>
        <option value="DCThide">DCT</option>
        <option value="DWThide">DWT</option>
      </select>
    </div>
  );
}


export default Chooser;
