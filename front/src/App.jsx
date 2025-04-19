import './index.css';
import React from "react";
import Footer from "./Footer.jsx";
import Header from "./Header.jsx";
import Title from "./title.jsx";

import Bg from './bg.jsx';
import Splinescene from './spline.jsx';
import ImageUploader from './ImageUploader.jsx';
import Container from './Container.jsx';
import TextBox from './Textcontainer.jsx';
function App() {
  return (
    <>
     <h1>Upload an Image</h1>
     <ImageUploader />
     <TextBox />
   <Splinescene/>
    <Container/>
    <Title/>
    <Header />
    <Bg />
    {/*<Footer/>*/}
   </>
  );
}
export default App;