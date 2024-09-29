'use client';

import {
    Box,
    TextField,
    Toolbar,
    Typography,
    Divider,
    Stack,
    Autocomplete,
    IconButton,
    Tooltip
} from '@mui/material';
import AddIcon from '@mui/icons-material/Add';
import {useRouter} from 'next/navigation';

export default function Page() {
    const router = useRouter();

    return (
        <Box>
            {/* Info */}
            <Toolbar>
                <Typography
                    variant={'h6'}
                >
                    Add new chat
                </Typography>
            </Toolbar>

            <Divider/>

            <Stack
                marginTop={2}
                gap={2}
            >
                {/* CHAT */}

                <Box
                    display={'flex'}
                    flexDirection={'row'}
                    gap={2}
                    width={'33%'}
                >
                    {/* Chat name */}
                    <TextField
                        label={'Chat name'}
                        sx={{flexGrow: 1}}
                    />
                </Box>

                {/* SYSTEM PROMPT*/}
                <Typography>
                    System Prompt
                </Typography>
                <Divider/>

                <Box
                    display={'flex'}
                    flexDirection={'row'}
                    gap={2}
                    width={'50%'}
                >
                    {/* Chat name */}
                    <TextField
                        label={'System prompt'}
                        multiline={true}
                        minRows={16}
                        sx={{flexGrow: 1}}
                    />
                </Box>


                {/* CREDENTIAL PROVIDERS*/}
                <Typography>
                    Credential Providers
                </Typography>
                <Divider/>

                <Box
                    display={'flex'}
                    flexDirection={'row'}
                    gap={2}
                    width={'50%'}
                >
                    {/*LLM*/}
                    <Autocomplete
                        renderInput={
                            (params) => <TextField {...params} label={'LLM Provider'}/>
                        }
                        options={['OpenAI', 'Anthropic']}
                        sx={{flexGrow: 0.5}}
                    />

                    {/*Embedding model*/}
                    <Autocomplete
                        renderInput={
                            (params) => <TextField {...params} label={'Embedding Model Provider'}/>
                        }
                        options={['OpenAI', 'Anthropic']}
                        sx={{flexGrow: 0.5}}
                    />

                    <Tooltip title={'Add new credential provider'}>
                        <IconButton
                            edge={'start'}
                            onClick={() => router.push('/credentials')}
                        >
                            <AddIcon/>
                        </IconButton>
                    </Tooltip>
                </Box>
            </Stack>
        </Box>
    );
}