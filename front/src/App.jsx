// App.jsx
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import Contact from './pages/Contact';
import FAQ from './pages/FAQ';
import './index.css';
import CustomCursor from './components/CustomCursor';

function App() {
  return (
    <>
  
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        
        <Route path="/FAQ" element={<FAQ />} />
      </Routes>
    </BrowserRouter>
    
    <CustomCursor/></>
  );
}

export default App;
