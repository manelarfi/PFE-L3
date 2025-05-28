import React from "react";


function FaqText() {
  return (
    <>
       <div className="centered-container">

          <h1> What is steganography ?</h1>
          <p>Steganography is the practice of hiding secret information within <br/> non-secret data, such as images, audio files, or text, to conceal its existence. Unlike encryption, which scrambles data to make it unreadable without a key, steganography embeds the hidden message in a way that it appears normal, making it difficult to detect. It is often used for secure communication, digital watermarking, and data protection.</p>
  
       </div>

   <div className="centered-container1">

   <h1> How does it work ?</h1>
   <p>Steganography hides secret data within ordinary files by making subtle, imperceptible changes. For example, in images, data can be embedded by modifying pixel values slightly.<br/> This conceals the message’s existence, unlike encryption, which only scrambles data.</p>
   </div>
   </>
  );
}

export default FaqText;