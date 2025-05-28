import React, { useState } from "react";
import ResultModal from "../components/ResultModal.jsx";
import Footer from "../components/Footer.jsx";
import Header from "../components/Header.jsx";
import Bg from '../components/Bg.jsx';
import FaqText from "../components/FaqText.jsx";

function ResultsHide() {
  const [showModal, setShowModal] = useState(false);
  const [imageUrl, setImageUrl] = useState(""); // URL de l'image à afficher

  // Simule la réception de l'image du backend
  const handleShowResult = () => {
    // Ici tu mets l'URL reçue du backend (ex: après fetch/post)
    setImageUrl("https://via.placeholder.com/400x200.png?text=Image+du+Backend");
    setShowModal(true);
  };

  return (
    <>
      <FaqText />
      <Header />
      <Bg />
      <button onClick={handleShowResult}>Afficher le résultat</button>
      <ResultModal show={showModal} imageUrl={imageUrl} onClose={() => setShowModal(false)} />
    </>
  );
}
export default ResultsHide;