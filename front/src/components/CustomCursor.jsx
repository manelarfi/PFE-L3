import { useEffect, useState } from "react";

export default function CustomCursor() {
  const [position, setPosition] = useState({ x: 0, y: 0 });
  const [targetPosition, setTargetPosition] = useState({ x: 0, y: 0 });

  useEffect(() => {
    const move = (e) => {
      setTargetPosition({ x: e.clientX, y: e.clientY }); // Update target position
    };

    window.addEventListener("mousemove", move);
    return () => window.removeEventListener("mousemove", move);
  }, []);

  useEffect(() => {
    const follow = () => {
      setPosition((prev) => ({
        x: prev.x + (targetPosition.x - prev.x) * 0.1, 
        y: prev.y + (targetPosition.y - prev.y) * 0.1,
      }));
    };

    const animationFrame = requestAnimationFrame(follow);
    return () => cancelAnimationFrame(animationFrame);
  }, [targetPosition]);

  return (
    <div
      style={{
        position: "fixed",
        top: position.y,
        left: position.x,
        width: 20,
        height: 20,
        backgroundColor: "white",
        borderRadius: "50%",
        pointerEvents: "none",
        transform: "translate(-50%, -50%)",
        zIndex: 9999,
        transition: "background-color 0.3s ease",
      }}
    />
  );
}