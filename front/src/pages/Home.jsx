import './index.css';
import React from "react";
import Footer from "./components/Footer.jsx";
import Header from "./components/Header.jsx";
import Title from "./components/title.jsx";
import ShowContainer from "./components/ShowContainer.jsx";
import HideContainer from "./HideContainer.jsx";
import Bg from './components/Bg.jsx';
import Splinescene from './components/Spline.jsx';
import { BrowserRouter, Routes, Route } from 'react-router-dom';


function Home() {
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
export default Home;