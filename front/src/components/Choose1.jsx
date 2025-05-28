import React, { useState } from 'react';

function Chooser() {
  // This component allows the user to choose a method TO SHOW the data 
  const [selectedOption, setSelectedOption] = useState('');

  const handleChange = (e) => {
    const value = e.target.value;
    setSelectedOption(value);

    // Execute code based on selection
    if (value === 'LSBshow') {
      console.log("You chose Option 1");
      // Do something for option 1
    } else if (value === 'DCTshow') {
      console.log("You chose Option 2");
      // Do something for option 2
    } else if (value === 'DWTshow') {
      console.log("You chose Option 3");
      // Do something for option 3
    }
  };

  return (
    <div className="chooser1">
      <label htmlFor="selector">Choose your method: </label>
      <select id="selector" onChange={handleChange}>
        <option value="">-- Select --</option>
        <option value="LSBshow">LSB</option>
        <option value="DCTshow">DCT</option>
        <option value="DWTshow">DWT</option>
      </select>
    </div>
  );
}


export default Chooser;
