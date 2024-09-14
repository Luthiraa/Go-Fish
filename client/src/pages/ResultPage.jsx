import React, { useEffect, useState } from 'react';
import axios from 'axios';

export default function ResultPage() {
    const [summary, setSummary] = useState('');
    const [resources, setResources] = useState([]);
    const [loading, setLoading] = useState(true);
    const query = new URLSearchParams(window.location.search).get('query');

    useEffect(() => {
        if (query) {
            axios.post('/api/search_and_summarize', { query })
                .then(response => {
                    setSummary(response.data.summary);
                    setResources(response.data.resources);
                    setLoading(false);
                })
                .catch(error => {
                    console.error('Error fetching summary:', error);
                    setLoading(false);
                });
        } else {
            setLoading(false);
        }
    }, [query]);

    return (
        <div className="flex items-center justify-center min-h-screen p-8">
            <div className="bg-white p-8 rounded shadow-md w-full max-w-6xl h-screen">
                <div className='flex flex-col md:flex-row justify-between items-center'>
                    <img src="logoFIN.png" alt="Logo" className="h-8 w-auto mb-4 md:hidden" />
                    <h1 className="text-4xl font-bold mb-4">{query}</h1>
                    <img src="logoFIN.png" alt="Logo" className="h-8 w-auto max-md:hidden" />
                </div>
                {loading ? <p>Loading...</p> : (
                    <>
                        <p>{summary}</p>
                        <ul>
                            {resources.map((resource, index) => (
                                <li key={index}><a href={resource} target="_blank" rel="noopener noreferrer">{resource}</a></li>
                            ))}
                        </ul>
                    </>
                )}
            </div>
        </div>
    );
}