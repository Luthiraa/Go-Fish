import { FormControl } from "@mui/material"
import SearchIcon from '@mui/icons-material/Search';
import OutlinedInput from "@mui/material/OutlinedInput"
import InputAdornment from '@mui/material/InputAdornment';
import React, { useState } from 'react';
import ArrowCircleUpRoundedIcon from '@mui/icons-material/ArrowCircleUpRounded';
import Button from '@mui/material/Button';

export default function SearchPage() {

    const [inputValue, setInputValue] = useState('');
    const quickSearches = ["What is Go Fish?", "Who helped develop this?", "What is the purpose of this?"];

    const handleQuickSearchClick = (searchText) => {
        setInputValue(searchText);
    };
    const handleInputChange = (event) => {
        setInputValue(event.target.value);
    };

    const handleSearchSubmit = () => {
        // use input value to send to backend
    };

    const handleKeyPress = (event) => {
        if (event.key === 'Enter') {
            handleSearchSubmit();
        }
    };

    return (
        <div className="h-screen flex justify-center items-center">
            <div className="w-full max-w-md md:max-w-2xl lg:max-w-3xl">
                <img src="logoFIN.png" alt="Logo" className="w-full"/>
                <FormControl fullWidth sx={{ m: 1 }}>
                    <OutlinedInput
                        id="outlined-adornment-amount"
                        startAdornment={<InputAdornment position="start"><SearchIcon /></InputAdornment>}
                        endAdornment={
                            inputValue && (
                                <InputAdornment position="end">
                                    <ArrowCircleUpRoundedIcon onClick={handleSearchSubmit} style={{ cursor: 'pointer' }} />
                                </InputAdornment>
                            )
                        }
                        placeholder="Discover..."
                        value={inputValue}
                        onChange={handleInputChange}
                        onKeyPress={handleKeyPress}
                        sx={{
                            borderRadius: 100,
                            padding: '8px 30px', // Added padding to make the inside bigger
                            '& .MuiOutlinedInput-notchedOutline': {
                                borderColor: 'darkblue',
                                borderWidth: 2,
                            },
                            '&:hover': {
                                transition: 'all 0.3s',
                                boxShadow: '0 4px 8px rgba(0, 0, 0, 0.2)',
                            },
                            '&:hover .MuiOutlinedInput-notchedOutline': {
                                borderColor: 'darkblue',
                            },
                            '&.Mui-focused': {
                                boxShadow: '0 4px 8px rgba(0, 0, 0, 0.2)',
                            },
                            '&.Mui-focused .MuiOutlinedInput-notchedOutline': {
                                borderColor: 'darkblue',
                            },
                        }}
                    />
                </FormControl>
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