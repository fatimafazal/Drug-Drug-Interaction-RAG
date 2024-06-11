import React from 'react';

function ResultsDisplay({ result }) {
    // The existence check ensures that if result is undefined or null,
    // it won't cause an error when trying to access its properties.
    const hasResult = result && result.id && result.completion;

    return (
        <div>
            <h2>Results</h2>
            {hasResult ? (
                <div className="result-item">
                    {/* Display the id and completion from the result */}
                    <p>Complication: {result.completion}</p>
                </div>
            ) : (
                // Display a message if no results are available or a query hasn't been made
                <p>No results to display or query has not been made.</p>
            )}
        </div>
    );
}

export { ResultsDisplay };

