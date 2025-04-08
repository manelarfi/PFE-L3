import React, { useState } from "react";

function ImageUploader() {

  

  return (
   <div className="image-uploader">
    <input type="file" accept="image/*" onChange={(e) => {
    const file = e.target.files[0]; }} />
    </div>
  );
}

export default ImageUploader;