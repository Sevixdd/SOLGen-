import React from 'react';
import './Header.css'; // Make sure to create this CSS file for styling
import logo from './nft.png'

function Header() {
  return (
    <div className="header">
      <img src={logo} alt="Logo" className="logo" />
      <h1>SolGen</h1>
    </div>
  );
}

export default Header;
