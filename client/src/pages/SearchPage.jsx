import { FormControl } from "@mui/material"
import SearchIcon from '@mui/icons-material/Search';
import OutlinedInput from "@mui/material/OutlinedInput"
import InputAdornment from '@mui/material/InputAdornment';
import Icon from '@mui/material/Icon';
import React, { useState } from 'react';
import Button from '@mui/material/Button';

export default function SearchPage() {

    const [inputValue, setInputValue] = useState('');

    const handleInputChange = (event) => {
        setInputValue(event.target.value);
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
                                    
                                </InputAdornment>
                            )
                        }
                        placeholder="Discover..."
                        value={inputValue}
                        onChange={handleInputChange}
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
            </div>
        </div>
    );
}