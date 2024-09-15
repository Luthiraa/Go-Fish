import React, { useEffect, useState } from 'react';
import SailingRoundedIcon from '@mui/icons-material/SailingRounded';
import axios from 'axios';
import SearchBar from '../components/searchBar';
import ReactMarkdown from 'react-markdown';

export default function ResultPage() {
    const [summary, setSummary] = useState('');
    const [inputValue, setInputValue] = useState('');
    const [resources, setResources] = useState([]);
    const [image, setImage] = useState('');
    const [loading, setLoading] = useState(true);
    const query = new URLSearchParams(window.location.search).get('query');

    // Handle quick search click
    const handleQuickSearchClick = (searchText) => {
        setInputValue(searchText);
    };

    // Handle input change in search bar
    const handleInputChange = (event) => {
        setInputValue(event.target.value);
    };

    // Handle key press to submit search
    const handleKeyPress = (event) => {
        if (event.key === 'Enter') {
            handleSearchSubmit();
        }
    };

    // Handle search submission
    const handleSearchSubmit = () => {
        window.location.href = `/result?query=${encodeURIComponent(inputValue)}`;
        axios.post('/api/search', { query: inputValue });
    };

    // Fetch data (summary and resources) from the API
    useEffect(() => {
        const fetchData = async () => {
            if (query) {
                try {
                    const response = await axios.post('/api/search_and_summarize', { query });
                    setSummary(response.data.summary);  // Set summary from API
                    setResources(response.data.resources);  // Set resources from API
                    setImage(response.data.image_url);  // Set image from API
                    console.log(image);

                } catch (error) {
                    console.error('Error fetching summary:', error);
                } finally {
                    setLoading(false);  // End loading state
                }
            } else {
                setLoading(false);  // If no query, stop loading
            }
        };

        fetchData();
    }, [query]);

    return (
        <div className="flex flex-col items-center justify-center min-h-screen space-y-4">
            <div className='flex flex-col md:flex-row items-center w-full max-w-md md:max-w-2xl lg:max-w-3xl mt-1'>
                <a href="/">
                    <img src="logoFIN.png" alt="Logo" className="h-12 w-auto my-4 md:hidden" />
                </a>
                {/* Search bar for querying */}
                <SearchBar
                    inputValue={inputValue}
                    handleInputChange={handleInputChange}
                    handleKeyPress={handleKeyPress}
                    handleSearchSubmit={handleSearchSubmit}
                    handleQuickSearchClick={handleQuickSearchClick}
                />
                <img src="logoFIN.png" alt="Logo" className="h-12 w-auto ml-4 max-md:hidden cursor-pointer hover:scale-105 transition-all" onClick={(e) => window.location.href = "/"} />
            </div>
            <div className="bg-white p-8 rounded shadow-md w-full max-w-6xl overflow-y-scroll" style={{ height: "80svh" }}>
                <div className='flex flex-col md:flex-row items-center'>
                    {/* Display query as a title */}
                    <h1 className="text-4xl font-bold mb-4">{query}</h1>
                </div>
                {loading ? (
                    <div>
                        <SailingRoundedIcon className="animate-bounce text-blue-500 mx-auto mr-4 mt-6" sx={{ fontSize: 60 }} />
                        <h2 className='animate-pulse text-blue-800'>Searching for information...</h2>
                    </div>
                ) : (
                    <>
                    <div className='flex'>
                        {/* Render the summary as Markdown */}
                        <div>
                            <ReactMarkdown>{summary}</ReactMarkdown>
                        </div>
                        {/* Display the image */}
                        {image && (
                            <img src={image} alt="Result" className="mt-4 w-64 h-64 object-contain" />
                        )}
                    </div>

                        {/* Display the list of resources */}
                        <ul className="mt-4">
                            {Array.isArray(resources) && resources.map((resource, index) => (
                                <li key={index}>
                                    <a href={resource} target="_blank" rel="noopener noreferrer" className="text-blue-500 underline">
                                        {resource}
                                    </a>
                                </li>
                            ))}
                        </ul>
                    </>
                )}
            </div>
        </div>
    );
}
