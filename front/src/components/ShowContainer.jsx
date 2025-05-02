import React from "react";
import ImageUploader1 from "./ImageUploader1.jsx";


function ShowContainer() {
  return (
    <>
     <ImageUploader1 />
     <h1 className="show" >Extract your text</h1>
     <div className="container1">

     <h2 className="container-title">Add Your Image</h2>
    
    <button onClick={alert} className='submit-button1'>
        Submit
      </button>
   </div></>
  );
}

export default ShowContainer;