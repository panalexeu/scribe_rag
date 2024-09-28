import {Toolbar} from "@mui/material";
import {Divider} from "@mui/material";
import {Box} from "@mui/material";
import Typography from "@mui/material/Typography";
import IconButton from '@mui/material/IconButton';
import AddIcon from '@mui/icons-material/Add';
import SearchIcon from '@mui/icons-material/Search';
import TextField from '@mui/material/TextField';
import {InputAdornment} from "@mui/material";


export default function Page() {
    return (
        <Box padding={1}>
            <Toolbar>
                <Typography variant={'h6'}>Chats</Typography>

                {/* Search Bar*/}
                <TextField
                    sx={{marginLeft: 'auto'}}
                    variant={'standard'}
                    label={"Search..."}
                    slotProps = {
                        {
                            input: {
                                endAdornment: (
                                    <InputAdornment position={'end'}>
                                        <IconButton>
                                            <SearchIcon/>
                                        </IconButton>
                                    </InputAdornment>
                                )
                            }
                        }
                    }
                />

                <Divider orientation={'vertical'}/>
                <IconButton>
                    <AddIcon/>
                </IconButton>

            </Toolbar>
            <Divider/>
        </Box>
    );
}