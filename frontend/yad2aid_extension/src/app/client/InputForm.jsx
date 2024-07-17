'use client';
import { useRouter } from 'next/router';
import { useState } from 'react';
import { SendRequest } from '../server/SendRequest.js'

export default function InputForm() {
  const [squareMeters, setSquareMeters] = useState('');
  const [maxPrice, setMaxPrice] = useState('');
  const [numRooms, setNumRooms] = useState('');
  const [city, setCity] = useState('');
  const [results, setResults] = useState([]);
  const router = useRouter();

  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      const response = await SendRequest(squareMeters, maxPrice, numRooms, city);
      console.log(response);
      setResults(Array.isArray(response) ? response : []);
      router.push('/results'); // Redirect to the results page
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <label>
        Square Meters:
        <input
          type="number"
          value={squareMeters}
          onChange={(e) => setSquareMeters(e.target.value)}
        />
      </label>
      <br />
      <label>
        Max Price:
        <input
          type="number"
          value={maxPrice}
          onChange={(e) => setMaxPrice(e.target.value)}
        />
      </label>
      <br />
      <label>
        Number of Rooms:
        <input
          type="number"
          value={numRooms}
          onChange={(e) => setNumRooms(e.target.value)}
        />
      </label>
      <br />
      <label>
        City:
        <input
          type="text"
          value={city}
          onChange={(e) => setCity(e.target.value)}
        />
      </label>
      <br />
      <button type="submit">Search</button>
    </form>
  );
}