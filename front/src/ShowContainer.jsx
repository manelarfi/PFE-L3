import React from "react";
import ImageUploader1 from "./ImageUploader1.jsx";


function ShowContainer() {
  return (
    <>
     
     <div className="container1">
     <h2 className="container-title">Add Your Image</h2>
    <ImageUploader1 />
    <button onClick={alert} className='submit-button1'>
        Submit
      </button>
   </div></>
  );
}

export default ShowContainer;