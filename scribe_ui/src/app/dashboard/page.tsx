import {Toolbar} from "@mui/material";
import {Divider} from "@mui/material";
import {Box} from "@mui/material";
import Typography from "@mui/material/Typography";
import IconButton from '@mui/material/IconButton';
import AddIcon from '@mui/icons-material/Add';
import SearchIcon from '@mui/icons-material/Search';
import TextField from '@mui/material/TextField';
import {InputAdornment} from "@mui/material";
import Stack from '@mui/material/Stack';
import {Pagination} from '@mui/material';

import ChatItem from './components/ChatItem';

export default function Page() {
    const chats = ['Item1', 'Item2', 'Item3','Item4','Item5','Item6','Item7', 'Item8', 'Item9', 'Item10'];

    return (
        <Box padding={1}>
            {/*TOOLBAR*/}
            <Toolbar>
                <Typography
                    variant={'h6'}
                    paddingRight={1}
                >
                    Chats
                </Typography>

                {/* Search Bar*/}
                <TextField
                    sx={{
                        marginLeft: 'auto',
                    }}
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

                {/* Add chat button*/}
                <Divider orientation={'vertical'}/>
                <IconButton>
                    <AddIcon/>
                </IconButton>
            </Toolbar>
            <Divider/>

            {/* Chats */}
            <Stack
                divider={
                    <Divider/>
                }
            >
                {
                    chats.map(
                        (chat, _) => (
                            <ChatItem name={chat}/>
                        )
                    )
                }
            </Stack>

            {/* Pagination */}
            <Box display={"flex"} justifyContent={'flex-end'}>
                <Pagination count={10}/>
            </Box>
        </Box>
    );
}