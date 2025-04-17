import './index.css';
import React from "react";
import Footer from "./Footer.jsx";
import Header from "./Header.jsx";
import Title from "./title.jsx";

import Bg from './bg.jsx';
import Splinescene from './spline.jsx';
import ImageUploader from './ImageUploader.jsx';

function App() {
  return (
    <>
     <ImageUploader />
   <Splinescene/>
   
    <Title/>
    <Header />
    <Bg />
    {/*<Footer/>*/}
   </>
  );
}
export default App;