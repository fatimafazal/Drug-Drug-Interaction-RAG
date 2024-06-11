import React, { useState } from 'react';
import axios from 'axios';

function QueryForm({ setResult }) {
    const [queryText, setQueryText] = useState('');

    const handleSubmit = async (event) => {
        event.preventDefault();
        console.log('Sending query:', queryText);  // Log the text being sent to the API
        try {
            // Update the endpoint and parameters as necessary based on your FastAPI setup
            const response = await axios.get(`http://127.0.0.1:8000/query`, {
                params: { query_text: queryText }
            });
            console.log('Received response:', response.data);  // Log the response data from the API
            setResult(response.data);
        } catch (error) {
            console.error('Error fetching data:', error);
            setResult({ error: 'Failed to fetch results' });
        }
    };

    return (
        <form onSubmit={handleSubmit} className="Search-form">
            <input
                id="queryInput"
                className="Search-input"
                type="text"
                value={queryText}
                onChange={e => setQueryText(e.target.value)}
                placeholder=" Enter 'What is the interaction between [Drug1] and [Drug2]?' "
                required
            />
            <button className="Search-button" type="submit">Search</button>
        </form>
    );
}

export { QueryForm };
