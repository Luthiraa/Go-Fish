import React, { useState } from 'react';
import Button from '@mui/material/Button';
import './SearchPage.css';
import axios from "axios";
import SearchBar from '../components/searchBar';

export default function SearchPage() {

    const [inputValue, setInputValue] = useState('');
    const quickSearches = ["What is Go Fish?", "Who helped develop this?", "What is the purpose of this?"];
    // const createBubbles = () => {
    //     const bubbleContainer = document.createElement('div');
    //     bubbleContainer.className = 'bubble-container';
    //     document.body.appendChild(bubbleContainer);

    //     for (let i = 0; i < 20; i++) {
    //         const bubble = document.createElement('div');
    //         bubble.className = 'bubble';
    //         bubble.style.left = `${Math.random() * 100}vw`;
    //         bubble.style.top = `${Math.random() * 100}vh`;
    //         bubbleContainer.appendChild(bubble);
    //     }
    // };

    React.useEffect(() => {
        // createBubbles();
    }, []);
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

    return (
        <div className="h-screen flex justify-center items-center">
            <div className="w-full max-w-md md:max-w-2xl lg:max-w-3xl">
                <img src="logoFIN.png" alt="Logo" className="w-full"/>
                <SearchBar inputValue={inputValue} handleInputChange={handleInputChange} handleKeyPress={handleKeyPress} handleSearchSubmit={handleSearchSubmit} handleQuickSearchClick={handleQuickSearchClick}/>
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
        </div>
    );
}