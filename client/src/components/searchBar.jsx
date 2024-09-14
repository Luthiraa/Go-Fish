import { FormControl } from "@mui/material"
import SearchIcon from '@mui/icons-material/Search';
import OutlinedInput from "@mui/material/OutlinedInput"
import InputAdornment from '@mui/material/InputAdornment';
import ArrowCircleUpRoundedIcon from '@mui/icons-material/ArrowCircleUpRounded';

export default function SearchBar({inputValue, handleInputChange, handleKeyPress, handleSearchSubmit}) {
    return (
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
                            backgroundColor: 'white',
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
    )
};