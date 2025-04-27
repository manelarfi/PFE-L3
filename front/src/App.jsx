import './index.css';
import React from "react";
import Footer from "./Footer.jsx";
import Header from "./Header.jsx";
import Title from "./title.jsx";

import Bg from './bg.jsx';
import Splinescene from './spline.jsx';
import ImageUploader from './ImageUploader.jsx';
import ImageUploader1 from './ImageUploader1.jsx';
import Container from './Container.jsx';
import TextBox from './Textcontainer.jsx';
function App() {
  return (
    <>
   
     <ImageUploader />
     <ImageUploader1 />
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