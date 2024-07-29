'use client';

import { useSearchParams } from 'next/navigation';
import { useEffect, useState } from 'react';

const ResultsPage = () => {
  const searchParams = useSearchParams();
  const results = searchParams.get('results');
  const [parsedResults, setParsedResults] = useState([]);

  useEffect(() => {
    if (results) {
      try {
        const parsed = JSON.parse(results);
        setParsedResults(parsed);
      } catch (error) {
        console.error('Failed to parse results:', error);
      }
    }
  }, [results]);

  return (
    <div>
      <h1>Results</h1>
      {parsedResults.length > 0 ? (
        <pre>{JSON.stringify(parsedResults, null, 2)}</pre>
      ) : (
        <p>No results found.</p>
      )}
    </div>
  );
};

export default ResultsPage;