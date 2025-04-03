
function Header() {
  return (
    <header>
      <h2 onClick={() =>   alert("Button Clicked!")}>scrycto</h2>
      <nav>

        <ul>
          <li><a href="#home">Home</a></li>
          <li><a href="#about">About US</a></li>
          <li><a href="#contact">Contact</a></li>
          <li><a href="#faq">FAQ</a></li>
          </ul>
       </nav>   
       <hr/>
 </header>
  );
}
export default Header;