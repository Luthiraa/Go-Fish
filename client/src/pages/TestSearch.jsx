import React, { useState } from 'react';
import Button from '@mui/material/Button';
import './SearchPage.css';
import axios from "axios";
import SearchBar from '../components/searchBar';
import { OutlinedInput } from '@mui/material';
import SettingsRoundedIcon from '@mui/icons-material/SettingsRounded';

export default function SearchPage() {

    const [inputValue, setInputValue] = useState('');
    const [githubLink, setGithubLink] = useState('');
    const [predictiveResults, setPredictiveResults] = useState([]);
    const quickSearches = ["What is Go Fish?", "Who helped develop this?", "What is the purpose of this?"];

    React.useEffect(() => {
        // createBubbles();
    }, []);

    const handleQuickSearchClick = (searchText) => {
        setInputValue(searchText);
    };

    const handleInputChange = async (event) => {
        const value = event.target.value;
        setInputValue(value);

        if (value.length > 2) { // Fetch predictive results if input length is greater than 2
            try {
                const response = await axios.post('/api/predictive-search', { query: value });
                setPredictiveResults(response.data.results);
            } catch (error) {
                console.error("Error fetching predictive search results:", error);
            }
        } else {
            setPredictiveResults([]);
        }
    };

    const handleKeyPress = (event) => {
        if (event.key === 'Enter') {
            handleSearchSubmit();
        }
    };

    const handleSearchSubmit = () => {
        window.location.href = `/result?query=${encodeURIComponent(inputValue)}&githubLink=${encodeURIComponent(githubLink)}`;
        axios.post('/api/search', { query: inputValue, githubLink: githubLink });
    };

    const [isModalOpen, setIsModalOpen] = useState(false);

    const handleSettingsClick = () => {
        setIsModalOpen(true);
    };

    const handleCloseModal = () => {
        setIsModalOpen(false);
    };

    const handleApplyModal = (input) => {
        const githubUsername = input.split('github.com/')[1] || '';
        setGithubLink(githubUsername);
        setIsModalOpen(false);
    };

    const handlePredictiveResultClick = (result) => {
        setInputValue(result);
        setPredictiveResults([]);
    };

    return (
        <div className="h-screen flex justify-center items-center relative">
            <div className="w-full max-w-md md:max-w-2xl lg:max-w-3xl">
                <img src="logoFIN.png" alt="Logo" className="w-full"/>
                <SearchBar 
                    inputValue={inputValue} 
                    handleInputChange={handleInputChange} 
                    handleKeyPress={handleKeyPress} 
                    handleSearchSubmit={handleSearchSubmit} 
                    handleQuickSearchClick={handleQuickSearchClick}
                />
                {predictiveResults.length > 0 && (
                    <div className="predictive-results">
                        {predictiveResults.map((result, index) => (
                            <div 
                                key={index} 
                                className="predictive-result-item" 
                                onClick={() => handlePredictiveResultClick(result)}
                            >
                                {result}
                            </div>
                        ))}
                    </div>
                )}
                <div className="flex max-md:flex-wrap justify-center space-x-3 max-md:space-y-3 mt-3">
                    {quickSearches.map((searchText, index) => (
                    <Button 
                        key={index} 
                        onClick={() => handleQuickSearchClick(searchText)}
                        sx={{
                            borderRadius: '50px',
                            padding: '8px 30px',
                            backgroundColor: 'orange',
                            color: 'black',
                            textTransform: 'capitalize',
                            transition: 'all 0.3s',
                            '&:hover': {
                                transition: 'all 0.3s',
                                scale: 1.05,
                            },
                        }}
                    >
                        {searchText}
                    </Button>
                    ))}
                </div>
            </div>
            <div className="absolute bottom-4 left-4 cursor-pointer hover:rotate-180 transition-all" onClick={handleSettingsClick}>
                <SettingsRoundedIcon />
            </div>
            {isModalOpen && (
                <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50" onClick={handleCloseModal}>
                    <div className="bg-white p-4 rounded shadow-lg" onClick={(e) => e.stopPropagation()}>
                        <div className='flex align-middle'>
                            <img src="github.png" alt="Github: " className='h-8 w-auto mr-4' />
                            <OutlinedInput 
                                sx={{height: "32px"}} 
                                value={githubLink} 
                                onChange={(e) => setGithubLink(e.target.value)}
                            />
                        </div>
                        <button onClick={(e) => {handleApplyModal(githubLink)}} className="mt-4 px-4 py-2 bg-blue-500 text-white rounded">Apply Changes</button>
                    </div>
                </div>
            )}
        </div>
    );
}