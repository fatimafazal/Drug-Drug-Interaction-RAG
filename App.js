import React, { useState } from 'react';
import { QueryForm } from './components/QueryForm';
import { ResultsDisplay } from './components/ResultsDisplay';
import './App.css';

function App() {
  // State to store the results from the API
  const [result, setResult] = useState({});

  return (
    <div className="App">
      <div className="App-header">
        {/* Changed to div and added rounded corners and shadow */}
        <h1>Drug Interaction Checker</h1>
        {/* QueryForm component to submit queries */}
        {/* Ensure QueryForm has an input with the className="Search-input" */}
        <QueryForm setResult={setResult} />
        {/* Ensure there's a button with the className="Search-button" in QueryForm */}
      </div>
      <div className="Results">
        {/* ResultsDisplay component to show the results */}
        {/* Make sure ResultsDisplay has a white background and appropriate padding */}
        <ResultsDisplay result={result} />
      </div>
    </div>
  );
}

export default App;
