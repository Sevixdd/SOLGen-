import React, { useState, useRef } from 'react';
import AWS from 'aws-sdk';
import './DifferentContent.css';
import { postRequest } from './apiService';

function DifferentContent() {
  const fileInputRef = useRef(null);
  const [file, setFile] = useState(null);
  const [description, setDescription] = useState("");
  const [userID, setUserID] = useState("");
  const [name, setName] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Configure AWS S3


  AWS.config.update({
    region: 'ap-south-1', // Replace with your DynamoDB region
    credentials: new AWS.Credentials({
      accessKeyId: "AKIAQ3EGPPNKIMSTY64J", // Use environment variables
      secretAccessKey: "fH+BALS2qDrcLO5L7ZCdgeIorf5l9MEUWWmC1rpH",
    }),
  });
  
  const s3 = new AWS.S3({
    apiVersion: '2006-03-01',
    params: { Bucket: 'encode-music-bucket' } // Your bucket name
  });
  const corsParams = {
    Bucket: 'encode-music-bucket',
    CORSConfiguration: { // This is where the JSON format comes into play
      CORSRules: [
        {
          AllowedHeaders: ['*'],
          AllowedMethods: ['GET', 'PUT', 'POST', 'DELETE', 'HEAD'], // The methods you want to allow
          AllowedOrigins: ['http://localhost:3000'], // Origins you want to allow requests from
          ExposeHeaders: [],
          MaxAgeSeconds: 3000, // Optional
        },
      ],
    },
  };
  
  s3.putBucketCors(corsParams, function(err, data) {
    if (err) {
      console.log('Error', err);
    } else {
      console.log('Success', data);
    }
  });

  const handleUploadClick = () => {
    fileInputRef.current.click(); // Programmatically click the hidden file input
  };

  const handleFileChange = (event) => {
    setFile(event.target.files[0]); // Set selected file
  };

  const handleDescriptionChange = (event) => {
    setDescription(event.target.value); // Set description
  };

  const handleUserIDChange = (event) => {
    setUserID(event.target.value); // Set userID
  };

  const handleNameChange = (event) => {
    setName(event.target.value); // Set name
  };

  const handleUploadAndPost = async () => {
    console.log("called?")
    setLoading(true);
    setError(null);
    try {
      const response = await fetch('http://35.177.177.250:5000/api/generate/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ prompt: description })
      });
      console.log("triggered", description)
      if (!response.ok) {
        throw new Error('Failed to post data');
      }
      const data = await response.json();
      console.log('Response:', data);
      // Handle response data as needed...
    } catch (error) {
      setError('An error occurred while processing your request. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="differentContent">
      {/* <input
        placeholder="User ID"
        value={userID}
        onChange={handleUserIDChange}
        className="inputField"
      />
      <input
        placeholder="Name"
        value={name}
        onChange={handleNameChange}
        className="inputField"
      /> */}
      {/* <button className="uploadButton" onClick={handleUploadClick}>Upload Audio</button> */}
      <input
        type="file"
        ref={fileInputRef}
        onChange={handleFileChange}
        style={{ display: 'none' }}
        accept="audio/*"
      />
      <textarea placeholder="Describe your music" rows="5" value={description} onChange={handleDescriptionChange}></textarea>
      <div className="buttonsRow">
        <button className="actionButton">Listen</button>
        <button className="actionButton" onClick={handleUploadAndPost}>Post</button>
      </div>
      {loading && <p>Loading...</p>}
      {error && <p>{error}</p>}
    </div>
  );
}

export default DifferentContent;
