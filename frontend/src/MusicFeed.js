import React, { useState, useEffect } from 'react';
import AWS from 'aws-sdk';
import MusicCard from './MusicCard';
import './MusicFeed.css';

const colorPalette = [
  "#64c4ed", "#2772db", "#49beb7", "#ff5959",
  "#5f5dbd", "#5e87b8", "#7dace4", "#8971d0",
  // Add more colors as needed
];

function MusicFeed() {
  const [musicians, setMusicians] = useState([]);

  useEffect(() => {
    const docClient = new AWS.DynamoDB.DocumentClient();
    const params = {
      TableName: "user-music-table",
    };

    docClient.scan(params, (err, data) => {
      if (err) {
        console.error("Unable to read item. Error JSON:", JSON.stringify(err, null, 2));
      } else {
        //console.log(data)
        setMusicians(data.Items);
      }
    });
  }, []);

  return (
    <div className="musicFeed">
      {musicians.map((musician, index) => (
        <MusicCard
          key={musician.id}
          musician={musician}
          color={colorPalette[index % colorPalette.length]} // Cycle through the color palette
        />
      ))}
    </div>
  );
}

export default MusicFeed;
