import React from "react";
import ImageUploader from "./ImageUploader.jsx";
import TextBox from "./TextContainer.jsx";

function HideContainer() {
  return (
    <>
     <ImageUploader />

     <TextBox />
    <h1 className="hide" >Hide your text</h1>
      <div className="container">
      <h2 className="container-title">Add Your Image</h2>
      <h2 className="container-text-title">Add Your Text</h2>

   

    


   </div></>
  );
}

export default HideContainer;