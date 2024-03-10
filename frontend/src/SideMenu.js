import React from 'react';
import { Link } from 'react-router-dom';
import './SideMenu.css'; // Ensure this is correctly imported

function SideMenu() {
  return (
    <div className="sideMenu">
      <Link to="/">Home</Link>
      <Link to="/different-content">Create Music</Link>
      {/* Add more links as needed */}
    </div>
  );
}

export default SideMenu;
