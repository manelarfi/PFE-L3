import './index.css';
import React from "react";
import Footer from "./Footer.jsx";
import Header from "./Header.jsx";
import Title from "./title.jsx";
import ShowContainer from "./ShowContainer.jsx";
import HideContainer from "./HideContainer.jsx";
import Bg from './bg.jsx';
import Splinescene from './spline.jsx';

function App() {
  return (
    <>
     <Header />
    
     <Title/>
     <Splinescene/>
     <HideContainer/>
     <ShowContainer/>
     
     <Bg />
    {/*<Footer/>*/}
   </>
  );
}
export default App;