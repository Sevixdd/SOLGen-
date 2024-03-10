const BASE_URL = 'http://35.177.177.250:5000/api/generate/';

export const postRequest = async (BASE_URL, body) => {
  try {
    const requestOptions = {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body)
    };

    const response = await fetch(`${BASE_URL}${endpoint}`, requestOptions);
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    
    return await response.json();
  } catch (error) {
    console.error('Error:', error);
    throw new Error('An error occurred while processing the request.');
  }
};