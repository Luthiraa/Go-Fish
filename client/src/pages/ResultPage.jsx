import React, { useEffect, useState } from 'react';
import SailingRoundedIcon from '@mui/icons-material/SailingRounded';
import axios from 'axios';
import SearchBar from '../components/searchBar';
import AsyncScriptLoader from 'react-async-script';
import ReactMarkdown from 'react-markdown';
import ArrowForwardIosRoundedIcon from '@mui/icons-material/ArrowForwardIosRounded';
import SyntaxHighlighter from 'react-syntax-highlighter';
import docco from 'react-syntax-highlighter/dist/esm/styles/hljs/docco';

export default function ResultPage() {
    const [summary, setSummary] = useState('');
    const [detailed, setDetailed] = useState('');
    const [inputValue, setInputValue] = useState('');
    const [resources, setResources] = useState([]);
    const [image, setImage] = useState('');
    const [reddit, setReddit] = useState({});
    const [loading, setLoading] = useState(true);
    const [snippet, setSnippet] = useState('');
    const [lineNumber, setLineNumber] = useState('');
    const [fileUrl, setFileUrl] = useState('');
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

    const RedditEmbed = AsyncScriptLoader(
        'https://embed.redditmedia.com/widgets/platform.js'
    )(({ isScriptLoadSucceed }) => {
        if (isScriptLoadSucceed && reddit.html) {
            return (
                <div
                    dangerouslySetInnerHTML={{ __html: reddit.html }}
                    className="reddit-embed mt-4"
                    style={{ transform: 'scale(0.2)', transformOrigin: 'top left' }}
                />
            );
        }
        return null;
    });

    // Fetch data (summary and resources) from the API
    useEffect(() => {
        const fetchData = async () => {
            if (query) {
                try {
                    const response = await axios.post('/api/search_and_summarize', { query });
                    setSummary(response.data.summary);  // Set summary from API
                    setResources(response.data.resources);  // Set resources from API
                    setImage(response.data.image_url);  // Set image from API
                    setReddit(response.data.reddit_embed || {});
                    setSnippet(response.data.snippet);  // Set snippet from API
                    setLineNumber(response.data.line_number);  // Set line number from API
                    setFileUrl(response.data.file_url);  // Set file URL from API
                    setDetailed(response.data.detailed);
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
                        {snippet && lineNumber && fileUrl && (
                            <div className="bg-[#24292e] p-4 rounded-xl mb-4">
                                <h2 className="text-xl font-semibold mb-2 text-white">GitHub Code Snippet</h2>
                                <p className='text-white'>Found in line: {lineNumber}</p>
                                <p className='text-white pb-2'>URL: <a href={fileUrl} target="_blank" rel="noopener noreferrer" className="text-[#2dba4e] underline">{fileUrl}</a></p>
                                <pre className="bg-[#5f6872] p-2 rounded"><SyntaxHighlighter language="javascript" style={docco}>{snippet}</SyntaxHighlighter></pre>
                            </div>
                        )}
                       <div className='grid grid-cols-1 md:grid-cols-3 gap-4'>
                {/* Left Column (Summary + Reddit Embed) */}
                <div className='md:col-span-2 flex flex-col'>
                    {/* Render the summary as Markdown */}
                    <ReactMarkdown>{summary}</ReactMarkdown>
                    {/* Display the Reddit embed under the summary */}
                    <div className='mt-4'>
                        <div
                            dangerouslySetInnerHTML={{ __html: reddit.html }}
                            className="reddit-embed"
                        />
                        <RedditEmbed />
                    </div>
                    <ReactMarkdown>{detailed}</ReactMarkdown>
                </div>
                {/* Right Column (Image) */}
                <div className='flex justify-center'>
                    {image && (
                        <img src={image} alt="Result" className="mt-4 w-64 h-64 object-contain" />
                    )}
                </div>
            </div>
            {/* Resources */}
            <h1 className='text-2xl font-medium mt-6'>Resources: </h1>
                        <ul className="mt-4">
                            {Array.isArray(resources) && resources.map((resource, index) => (
                                <li key={index} className="flex items-center py-1">
                                    <ArrowForwardIosRoundedIcon className='text-blue-500' sx={{ fontSize: 16 }} />
                                    <a href={resource} target="_blank" rel="noopener noreferrer" className="text-blue-500 underline ml-1">
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