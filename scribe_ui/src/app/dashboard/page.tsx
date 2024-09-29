import {
    Toolbar,
    Divider,
    Box,
    Typography,
    IconButton,
    TextField,
    InputAdornment,
    Stack,
    Pagination,
    Tooltip
} from '@mui/material';
import AddIcon from '@mui/icons-material/Add';
import SearchIcon from '@mui/icons-material/Search';

import ChatItem from './components/ChatItem';

export default function Page() {
    const chats = ['Item1', 'Item2', 'Item3', 'Item4', 'Item5', 'Item6', 'Item7', 'Item8', 'Item9', 'Item10'];

    return (
        <Box>
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
                    slotProps={
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

                {/* Add chat button*/}
                <Tooltip title={'Add new chat'}>
                    <IconButton>
                        <AddIcon/>
                    </IconButton>
                </Tooltip>
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