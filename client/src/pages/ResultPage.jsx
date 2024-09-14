import React, { useEffect, useState } from 'react';
import SailingRoundedIcon from '@mui/icons-material/SailingRounded';
import axios from 'axios';

export default function ResultPage() {
    const [summary, setSummary] = useState('');
    const [resources, setResources] = useState([]);
    const [loading, setLoading] = useState(true);
    const query = new URLSearchParams(window.location.search).get('query');

    useEffect(() => {
        const fetchData = async () => {
            if (query) {
                try {
                    const response = await axios.post('/api/search_and_summarize', { query });
                    setSummary(response.data.summary);
                    setResources(response.data.resources);
                } catch (error) {
                    console.error('Error fetching summary:', error);
                } finally {
                    setLoading(false);
                }
            } else {
                setLoading(false);
            }
        };

        fetchData();
    }, [query]);

    return (
        <div className="flex items-center justify-center min-h-screen p-8">
            <div className="bg-white p-8 rounded shadow-md w-full max-w-6xl h-screen">
                <div className='flex flex-col md:flex-row justify-between items-center'>
                    <img src="logoFIN.png" alt="Logo" className="h-8 w-auto mb-4 md:hidden" />
                    {/* query/ TITLE*/}
                    <h1 className="text-4xl font-bold mb-4">{query}</h1>
                    <img src="logoFIN.png" alt="Logo" className="h-8 w-auto max-md:hidden" />
                </div>
                {loading ? <div>
                    <SailingRoundedIcon className="animate-bounce text-blue-500 mx-auto mr-4 mt-6" sx={{ fontSize: 60 }}/>
                    <h2 className='animate-pulse text-blue-800'>Searching for information...</h2>
                </div> : (
                    <>
                        <p>{summary}</p>
                        <ul>
                            {Array.isArray(resources) && resources.map((resource, index) => (
                                <li key={index}><a href={resource} target="_blank" rel="noopener noreferrer">{summary}</a></li>
                            ))}
                        </ul>
                    </>
                )}
            </div>
        </div>
    );
}