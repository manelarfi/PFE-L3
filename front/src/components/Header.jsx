
        // pages/Home.jsx
        import { useNavigate } from 'react-router-dom';
function Header() {

const navigate = useNavigate();
  const handleContact = () => {
    navigate('/Contact'); // changes the URL and shows About page
      
    };

  const navigate1 = useNavigate();
  const handleFAQ = () => {
    navigate('/FAQ'); // changes the URL and shows About page
  };

  const navigate2 = useNavigate();
  const handleHome = () => {
    navigate('/'); // changes the URL and shows About page
  };

  return (
    <header>

      <nav>
         <ul>

           <li> <button onClick={handleHome}>Home</button></li>
           <li> <button onClick={handleContact}>Contact</button></li>
           <li> <button onClick={handleFAQ}>FAQ</button></li>
          
         </ul>
      </nav>   

       
       <div className="logo">
     
        <img src="/scrycto.svg" alt="Logo" />
      

    </div>
       
 </header>
  );
}
export default Header;