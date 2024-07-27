'use client';
import { useRouter } from 'next/navigation';
import { useState } from 'react';
import { sendRequest } from '../server/SendRequest';

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
      const userName = 'Orian';
      const swipe = 'right';
      
      const userData = { user_name: userName };
        const aptFilterData = { 
            price: parseInt(maxPrice), 
            city: city, 
            sqm: parseInt(squareMeters), 
            rooms: parseInt(numRooms)
        };
        const swipeData = { swipe: swipe }

        console.log('Request Data:', { user: userData, apt_filter: aptFilterData, swipe: swipeData });
        const response = await sendRequest(userData, aptFilterData, swipeData);
        console.log('Response:', response);

      // const formattedResults = Array.isArray(response) ? response : [];
      setResults(response);

    //   //ONLY TO CHECK pages before connecting to backend 
    //   const formResults = [
    //     { squareMeters, maxPrice, numRooms, city }
    //   ];
    //   setResults(formResults);

      // Redirect to the results page with the results as a query parameter
      // const queryString = new URLSearchParams({ results: JSON.stringify(formResults) }).toString();
      // router.push(`/results?${queryString}`);
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <div>
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
    {results && (
      <iframe
        src={results}
        width="100%"
        height="500px"
        style={{ border: 'none' }}
        title="Embedded Webpage"
      ></iframe>
    )}
  </div>
  );
}
