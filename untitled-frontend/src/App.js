import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [carReg, setCarReg] = useState('');
  const [startingPoint, setStartingPoint] = useState('');
  const [destination, setDestination] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await axios.post('API URL HERE', {
        carReg,
        startingPoint,
        destination,
      });

      console.log(response.data); // Optional: Display the response data

      // Reset the form
      setCarReg('');
      setStartingPoint('');
      setDestination('');
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div>
      <h1>Untitled React App</h1>
      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="carReg">Car Registration:</label>
          <input
            type="text"
            id="carReg"
            value={carReg}
            onChange={(e) => setCarReg(e.target.value)}
          />
        </div>
        <div>
          <label htmlFor="startingPoint">Starting Point:</label>
          <input
            type="text"
            id="startingPoint"
            value={startingPoint}
            onChange={(e) => setStartingPoint(e.target.value)}
          />
        </div>
        <div>
          <label htmlFor="destination">Destination:</label>
          <input
            type="text"
            id="destination"
            value={destination}
            onChange={(e) => setDestination(e.target.value)}
          />
        </div>
        <button type="submit">Submit</button>
      </form>
    </div>
  );
}

export default App;

