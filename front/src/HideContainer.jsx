import React from "react";
import ImageUploader from "./ImageUploader.jsx";
import TextBox from "./TextContainer.jsx";

function HideContainer() {
  return (
    <>
    <h1 className="hide" >hide your text</h1>
      <div className="container">
      <h2 className="container-title">Add Your Image</h2>
      <h2 className="container-text-title">Add Your Text</h2>

    <ImageUploader />

    <TextBox />


   </div></>
  );
}

export default HideContainer;