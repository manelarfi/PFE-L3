import './index.css';
import React from "react";
import Footer from "./Footer.jsx";
import Header from "./Header.jsx";
import Title from "./title.jsx";

import Bg from './bg.jsx';
import Splinescene from './spline.jsx';

function App() {
  return (
    <> 
   <Splinescene/>
   
    <Title/>
    <Header />
    <Bg />
     
   </>
  );
}
export default App;