import '../index.css';
import React from "react";
import Footer from "../components/Footer.jsx";
import Header from "../components/Header.jsx";
import Bg from '../components/Bg.jsx';
import FaqText from "../components/FaqText.jsx";
 

import { BrowserRouter, Routes, Route } from 'react-router-dom';


function FAQ() {
  return (
    <>
     <FaqText/>
     
     <Header/>
     <Bg/>
    
    </>);
  }
  export default FAQ;