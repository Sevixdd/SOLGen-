import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Header from './Header';
import SideMenu from './SideMenu';
import MusicFeed from './MusicFeed';
import DifferentContent from './DifferentContent'; // This is the new component you will create
import './App.css';
import AWS from 'aws-sdk';

AWS.config.update({
  region: 'ap-south-1', // Replace with your DynamoDB region
  credentials: new AWS.Credentials({
    accessKeyId: "AKIAQ3EGPPNKIMSTY64J", // Use environment variables
    secretAccessKey: "fH+BALS2qDrcLO5L7ZCdgeIorf5l9MEUWWmC1rpH",
  }),
});

function App() {
  return (
    <Router>
      <div className="appContainer">
        <Header />
        <div className="mainContent">
          <SideMenu />
          <Routes>
            <Route path="/" element={<MusicFeed />} />
            <Route path="/different-content" element={<DifferentContent />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;
