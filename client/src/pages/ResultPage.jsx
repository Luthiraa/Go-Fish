import React, { useEffect, useState } from 'react';
import axios from 'axios';

export default function ResultPage() {
    const [endpoint, setEndpoint] = useState('');
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        //! hardcoded endpoint
        axios.get('/api/summ')
            .then(response => {
                setEndpoint(response.data.endpoint);
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