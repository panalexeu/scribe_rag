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
    Tooltip,
    Button,
    Select,
    MenuItem,
    FormControl,
    InputLabel
} from '@mui/material';
import AddIcon from '@mui/icons-material/Add';
import UploadFileIcon from '@mui/icons-material/UploadFile';
import {useRouter} from 'next/navigation';
import {useState} from "react";

export default function Page() {
    const router = useRouter();
    const [chatType, setChatType] = useState('Instruction');

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

                    {/* Chat type*/}
                    <FormControl>
                        <InputLabel>Chat Type</InputLabel>
                        <Select
                            value={chatType}
                            onChange={
                                (event) => setChatType(event.target.value)
                            }
                            sx={{flexGrow: 1}}
                            label={'Chat Type'}
                        >
                            <MenuItem value={'Instruction'}>Instruction</MenuItem>
                            <MenuItem value={'History'}>History</MenuItem>
                        </Select>
                    </FormControl>
                </Box>

                {/* Chat description*/}
                <Box
                    display={'flex'}
                    flexDirection={'row'}
                    gap={2}
                    width={'33%'}
                >
                    <TextField
                        label={'Chat description'}
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
                        sx={{flexGrow: 1}}
                    />

                    {/*Embedding model*/}
                    <Autocomplete
                        renderInput={
                            (params) => <TextField {...params} label={'Embedding Model Provider'}/>
                        }
                        options={['OpenAI', 'Anthropic']}
                        sx={{flexGrow: 1}}
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

                {/*DOCUMENTS*/}
                <Typography>
                    Documents
                </Typography>
                <Divider/>

                <Box
                    display={'flex'}
                    justifyContent={'end'}
                >
                    <Button
                        variant={'outlined'}
                        startIcon={<UploadFileIcon/>}
                    >
                        Upload Documents
                    </Button>
                </Box>

            </Stack>
        </Box>
    );
}