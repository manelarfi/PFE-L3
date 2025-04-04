import './index.css';
import React from "react";
import Footer from "./Footer.jsx";
import Header from "./Header.jsx";
import Title from "./title.jsx";
import Logo from './logo.jsx';
import Bg from './bg.jsx';
import Splinescene from './spline.jsx';

function App() {
  return (
    <> 
   <Splinescene/>
    <Logo />
    <Title/>
    <Header />
    <Bg />
     
   </>
  );
}
export default App;