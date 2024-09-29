'use client';

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
import { useRouter } from 'next/navigation';

import ChatItem from './components/ChatItem';

export default function Page() {
    const chats = ['Item1', 'Item2', 'Item3', 'Item4', 'Item5', 'Item6', 'Item7', 'Item8', 'Item9', 'Item10'];
    const router = useRouter();

    return (
        <Box>
            {/*TOOLBAR*/}
            <Toolbar>
                {/* Name */}
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

                {/* Add chat button*/}
                <Tooltip
                    title={'Add new chat'}
                >
                    <IconButton
                        onClick={
                            () => {
                                router.push('/dashboard/add-new-chat');
                            }
                        }
                        edge={'end'}
                    >
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