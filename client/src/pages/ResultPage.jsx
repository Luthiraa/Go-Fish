import React, { useEffect, useState } from 'react';

export default function ResultPage() {
    const [endpoint, setEndpoint] = useState('');

    useEffect(() => {
        fetch('http://localhost:5000/api/github')  // Ensure the URL matches your Flask backend
            .then(response => response.json())
            .then(data => setEndpoint(data.endpoint))
            .catch(error => console.error('Error fetching endpoint:', error));
    }, []);

    return (
        <div>
            <h1>Result Page</h1>
            <p>Endpoint: {endpoint}</p>
        </div>
    );
}