import React from 'react';
import './MusicCard.css';
import { useState } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faPlay, faPause, faStop } from '@fortawesome/free-solid-svg-icons';

function MusicCard({ musician, color }) {
  const [audio, setAudio] = useState(new Audio(musician.audioUrl));

  const playAudio = () => {
    audio.play();
  };

  const pauseAudio = () => {
    audio.pause();
  };

  const stopAudio = () => {
    audio.pause();
    audio.currentTime = 0;
  };

  return (
    <div className="musicCard" style={{ backgroundColor: color }}>
      <h2>{musician.name}</h2>
      {/* <p>User ID: {musician.userID}</p>
      <p>Followers: {musician.followers.toLocaleString()}</p>
      <p>Rating: {musician.rating} / 5</p> */}
      <div className="buttons">
        <button onClick={playAudio}><FontAwesomeIcon icon={faPlay} /> Play Music</button>
        <button onClick={pauseAudio}><FontAwesomeIcon icon={faPause} /> Pause Music</button>
        <button onClick={stopAudio}><FontAwesomeIcon icon={faStop} /> Stop Music</button>
      </div>
    </div>
  );
}

export default MusicCard;
