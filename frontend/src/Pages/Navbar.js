import { Outlet, Link } from "react-router-dom";
import './Navbar.css'

const Navbar = () => {
  return (
    <>
      <nav className="navbar">
        <h2 className="title">Some App</h2>
        <ul className="links">
          <li>
            <Link to="/map" className='routes'>Map</Link>
          </li>
          <li>
            <Link to="/" className='routes'>Table</Link>
          </li>
        </ul>
      </nav>

      <Outlet />
    </>
  )
};

export default Navbar;