import './index.css';
import React from "react";
import Footer from "./Footer.jsx";
import Header from "./Header.jsx";
import Title from "./title.jsx";
import Logo from './logo.jsx';
import bg from './bg.jsx';
function App() {
  return (
    <> 
    <Logo />
    <bg />
    <Header />
    <Title/>
    <Footer/>
   </>
  );
}
export default App;