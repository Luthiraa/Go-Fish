import React, { useEffect, useState } from 'react';
import SailingRoundedIcon from '@mui/icons-material/SailingRounded';
import axios from 'axios';
import SearchBar from '../components/searchBar';

export default function ResultPage() {
    const [summary, setSummary] = useState('');
    const [inputValue, setInputValue] = useState('');
    const [resources, setResources] = useState([]);
    const [loading, setLoading] = useState(true);
    const query = new URLSearchParams(window.location.search).get('query');

    const handleQuickSearchClick = (searchText) => {
        setInputValue(searchText);
    };
    const handleInputChange = (event) => {
        setInputValue(event.target.value);
    };

    const handleKeyPress = (event) => {
        if (event.key === 'Enter') {
            handleSearchSubmit();
        }
    };

    const handleSearchSubmit = () => {
        window.location.href = `/result?query=${encodeURIComponent(inputValue)}`;
        axios.post('/api/search', { query: inputValue })
    };

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
        <div className="flex flex-col items-center justify-center min-h-screen space-y-4">
            <div className='flex flex-col md:flex-row items-center w-full max-w-md md:max-w-2xl lg:max-w-3xl mt-1'>
                <img src="logoFIN.png" alt="Logo" className="h-12 w-auto my-4 md:hidden" />
                <SearchBar inputValue={inputValue} handleInputChange={handleInputChange} handleKeyPress={handleKeyPress} handleSearchSubmit={handleSearchSubmit} handleQuickSearchClick={handleQuickSearchClick} />
                <img src="logoFIN.png" alt="Logo" className="h-12 w-auto ml-4 max-md:hidden" />
            </div>
            <div className="bg-white p-8 rounded shadow-md w-full max-w-6xl overflow-y-scroll" style={{height: "80svh"}}>
                <div className='flex flex-col md:flex-row items-center'>
                    <h1 className="text-4xl font-bold mb-4">{query}</h1>
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