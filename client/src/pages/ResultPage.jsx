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
        <div className="flex items-center justify-center min-h-screen p-8">
            <div className="bg-white p-8 rounded shadow-md w-full max-w-6xl h-screen">
                <div className='flex flex-col md:flex-row justify-between items-center'>
                    <img src="logoFIN.png" alt="Logo" className="h-8 w-auto mb-4 md:hidden" />
                    <h1 className="text-4xl font-bold mb-4">{new URLSearchParams(window.location.search).get('query')}</h1>
                    <img src="logoFIN.png" alt="Logo" className="h-8 w-auto max-md:hidden" />
                </div>
                {loading ? <p>Loading...</p> : <p>Endpoint: {endpoint}</p>}
            </div>
        </div>
    );
}