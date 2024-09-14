import React, { useEffect, useState } from 'react';

export default function ResultPage() {
    const [endpoint, setEndpoint] = useState('');
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetch('/repos')
            .then(response => response.json())
            .then(data => {
                setEndpoint(data.endpoint);
                setLoading(false);
            })
            .catch(error => {
                console.error('Error fetching endpoint:', error);
                setLoading(false);
            });
    }, []);

    return (
        <div>
            <h1>Result Page</h1>
            {loading ? <p>Loading...</p> : <p>Endpoint: {endpoint}</p>}
        </div>
    );
}