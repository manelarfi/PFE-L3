import React from "react";

function ResultModal({ show, imageUrl, onClose }) {
  if (!show) return null;

  return (
    <div style={{
      position: "fixed", top: 0, left: 0, width: "100vw", height: "100vh",
      background: "rgba(0,0,0,0.5)", display: "flex", alignItems: "center", justifyContent: "center", zIndex: 1000
    }}>
      <div style={{
        background: "#fff", padding: 24, borderRadius: 8, textAlign: "center", minWidth: 300
      }}>
        <h2>Résultat</h2>
        <img src={imageUrl} alt="Résultat" style={{ maxWidth: "100%", marginBottom: 16 }} />
        <br />
        <a href={imageUrl} download="result.png">
          <button>Télécharger l'image</button>
        </a>
        <br /><br />
        <button onClick={onClose}>Fermer</button>
      </div>
    </div>
  );
}

export default ResultModal;