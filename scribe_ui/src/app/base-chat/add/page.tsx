'use client';

import {
    Box, Breadcrumbs, Divider, Link as MUILink, Typography, TextField, InputAdornment, IconButton, Button, Snackbar
} from '@mui/material';
import {useRouter} from 'next/navigation';
import Link from "next/link";
import {useState, useEffect} from "react";
import ClearIcon from '@mui/icons-material/Clear';

import {BaseChatPostModel} from "@/src/app/base-chat/models";
import {SysPromptResponseModel} from "@/src/app/sys-prompt/models";
import {ChatModelResponseModel} from "@/src/app/chat-model/models";
import {VectorCollectionResponseModel} from "@/src/app/vec-col/models";
import {API_URL, TABLE_PAGE_LIMIT} from "@/src/constants";

// Import table components
import {SysPromptTable, ChatModelTable, VecColTable} from "../components/tables"; // Adjust the import path as needed

export default function Page() {
    const router = useRouter();
    const [openSnackbar, setOpenSnackbar] = useState(false);
    const [snackbarMessage, setSnackbarMessage] = useState('');

    const [name, setName] = useState(null);
    const [desc, setDesc] = useState(null);
    const [sysPrompt, setSelectedSysPrompt] = useState<SysPromptResponseModel>(null);
    const [chatModel, setSelectedChatModel] = useState<ChatModelResponseModel>(null);
    const [vecCol, setSelectedVecCol] = useState<VectorCollectionResponseModel>(null);

    // SYS PROMPT
    const [sysPromptPage, setSysPromptPage] = useState(1);
    const [sysPromptCount, setSysPromptCount] = useState(0);
    const [sysPrompts, setSysPrompts] = useState<SysPromptResponseModel[]>([]);

    async function fetchSysPromptCount() {
        try {
            const response = await fetch(
                `${API_URL}/sys-prompt/count`,
                {
                    method: 'GET'
                }
            );

            if (response.status === 200) {
                const data = await response.json();
                setSysPromptCount(data);
            } else {
                setSnackbarMessage(`something went wrong 😢, status code: ${response.status}`);
                setOpenSnackbar(true);
            }
        } catch (error) {
            setSnackbarMessage(`something went wrong 😢, error: ${error.message}`);
            setOpenSnackbar(true);
        }
    }

    async function fetchSysPromptItems() {
        const offset = (sysPromptPage - 1) * TABLE_PAGE_LIMIT;

        try {
            const response = await fetch(
                `${API_URL}/sys-prompt/?limit=${TABLE_PAGE_LIMIT}&offset=${offset}`,
                {
                    method: 'GET'
                }
            );

            if (response.ok) {
                const data = await response.json();
                setSysPrompts(data);
            } else {
                setSnackbarMessage(`something went wrong 😢, status code: ${response.status}`);
                setOpenSnackbar(true);
            }
        } catch (error) {
            setSnackbarMessage(`something went wrong 😢, error: ${error.message}`);
            setOpenSnackbar(true);
        }
    }

    useEffect(() => {
        fetchSysPromptCount();
        fetchSysPromptItems();
    }, [sysPromptPage])


    // CHAT MODEL
    const [chatModelPage, setChatModelPage] = useState(1);
    const [chatModelCount, setChatModelCount] = useState(0);
    const [chatModels, setChatModels] = useState<ChatModelResponseModel[]>([]);

    async function fetchChatModelCount() {
        try {
            const response = await fetch(
                `${API_URL}/chat-model/count`,
                {
                    method: 'GET'
                }
            );

            if (response.status === 200) {
                const data = await response.json();
                setChatModelCount(data);
            } else {
                setSnackbarMessage(`something went wrong 😢, status code: ${response.status}`);
                setOpenSnackbar(true);
            }
        } catch (error) {
            setSnackbarMessage(`something went wrong 😢, error: ${error.message}`);
            setOpenSnackbar(true);
        }
    }

    async function fetchChatModelItems() {
        const offset = (chatModelPage - 1) * TABLE_PAGE_LIMIT;

        try {
            const response = await fetch(
                `${API_URL}/chat-model/?limit=${TABLE_PAGE_LIMIT}&offset=${offset}`,
                {
                    method: 'GET'
                }
            );

            if (response.ok) {
                const data = await response.json();
                setChatModels(data);
            } else {
                setSnackbarMessage(`something went wrong 😢, status code: ${response.status}`);
                setOpenSnackbar(true);
            }
        } catch (error) {
            setSnackbarMessage(`something went wrong 😢, error: ${error.message}`);
            setOpenSnackbar(true);
        }
    }

    useEffect(() => {
        fetchChatModelCount();
        fetchChatModelItems();
    }, [chatModelPage])

    // VECTOR STORE
    const [vecColPage, setVecColPage] = useState(1);
    const [vecColCount, setVecColCount] = useState(0);
    const [vecCols, setVecCols] = useState<VectorCollectionResponseModel[]>([]);

    async function fetchVecColCount() {
        try {
            const response = await fetch(
                `${API_URL}/vec-col/count`,
                {
                    method: 'GET'
                }
            );

            if (response.status === 200) {
                const data = await response.json();
                setVecColCount(data);
            } else {
                setSnackbarMessage(`something went wrong 😢, status code: ${response.status}`);
                setOpenSnackbar(true);
            }
        } catch (error) {
            setSnackbarMessage(`something went wrong 😢, error: ${error.message}`);
            setOpenSnackbar(true);
        }
    }

    async function fetchVecCols() {
        const offset = (vecColPage - 1) * TABLE_PAGE_LIMIT;

        try {
            const response = await fetch(
                `${API_URL}/vec-col/?limit=${TABLE_PAGE_LIMIT}&offset=${offset}`,
                {
                    method: 'GET'
                }
            );

            if (response.ok) {
                const data = await response.json();
                setVecCols(data);
            } else {
                setSnackbarMessage(`something went wrong 😢, status code: ${response.status}`);
                setOpenSnackbar(true);
            }
        } catch (error) {
            setSnackbarMessage(`something went wrong 😢, error: ${error.message}`);
            setOpenSnackbar(true);
        }
    }

    async function handleSubmit() {
        if (!name || !desc || !chatModel) {
            setSnackbarMessage(`fulfill name, desc and chat-model at least! 😡`);
            setOpenSnackbar(true);
            return;
        }

        try {
            const request = BaseChatPostModel.parse({
                name: name,
                desc: desc,
                chat_model_id: chatModel.id,
                system_prompt_id: !sysPrompt ? null : sysPrompt.id,
                vec_col_name: !vecCol ? null : vecCol.name
            });

            const response = await fetch(
                `${API_URL}/base-chat/`,
                {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(request)
                }
            );
            if (response.status == 201) {
                router.push('/base-chat');
            } else {
                setSnackbarMessage(`smth went wrong 😢, status code: ${response.status}`);
                setOpenSnackbar(true);
            }
        } catch (error) {
            setSnackbarMessage(`something went wrong 😢, error: ${error.message}`);
            setOpenSnackbar(true);
        }
    }

    useEffect(() => {
        fetchVecColCount();
        fetchVecCols();
    }, [vecColPage])

    return (
        <Box
            display={'flex'}
            flexDirection={"column"}
            alignItems={'flex-start'}
            gap={2}
        >
            {/*TOP PANEL*/}
            <Breadcrumbs>
                <Typography variant={'h6'}>
                    <MUILink
                        component={Link}
                        href={'/base-chat'}
                        underline={'none'}
                    >
                        base-chat
                    </MUILink>
                </Typography>
                <Typography variant={'h6'}>
                    add
                </Typography>
            </Breadcrumbs>

            <Divider sx={{width: '100%'}}/>

            {/* MAIN CONTENT */}
            <Box
                display={'flex'}
                flexDirection={'column'}
            >
                <Box
                    display={'flex'}
                    flexDirection={'column'}
                    gap={2}
                >
                    {/* NAME */}
                    <TextField
                        id={'name'}
                        variant={'standard'}
                        label={'name'}
                        value={name}
                        onChange={(e) => {
                            setName(e.target.value)
                        }}
                    />

                    {/* DESC */}
                    <TextField
                        id={'desc'}
                        label={'desc'}
                        value={desc}
                        multiline
                        rows={3}
                        onChange={(e) => {
                            setDesc(e.target.value)
                        }}
                    />
                </Box>
            </Box>

            <Divider sx={{width: '100%'}}/>

            {/*  TABLES  */}
            <Box>

                <Box
                    display={'flex'}
                    flexDirection={'row'}
                    gap={2}
                >
                    <TextField
                        id={'sys-prompt'}
                        variant={'outlined'}
                        label={'sys-prompt'}
                        value={!sysPrompt ? '' : sysPrompt.name}
                        sx={{width: '17%'}}
                        multiline={true}
                        InputProps={{
                            readOnly: true,
                            endAdornment: (
                                <InputAdornment position="end">
                                    <IconButton onClick={() => { /* handle click here */
                                        setSelectedSysPrompt(null);
                                    }}>
                                        <ClearIcon/>
                                    </IconButton>
                                </InputAdornment>
                            ),
                        }}
                    />

                    <TextField
                        id={'chat-model'}
                        variant={'outlined'}
                        label={'chat-model'}
                        value={!chatModel ? '' : chatModel.name}
                        multiline={true}
                        sx={{width: '23%'}}
                        InputProps={{
                            readOnly: true,
                            endAdornment: (
                                <InputAdornment position="end">
                                    <IconButton onClick={() => {
                                        setSelectedChatModel(null);
                                    }}>
                                        <ClearIcon/>
                                    </IconButton>
                                </InputAdornment>
                            ),
                        }}
                    />

                    <TextField
                        id={'vec-col'}
                        variant={'outlined'}
                        label={'vec-col'}
                        value={!vecCol ? '' : vecCol.name}
                        multiline={true}
                        sx={{width: '60%'}}
                        InputProps={{
                            readOnly: true,
                            endAdornment: (
                                <InputAdornment position="end">
                                    <IconButton onClick={() => {
                                        setSelectedVecCol(null);
                                    }}>
                                        <ClearIcon/>
                                    </IconButton>
                                </InputAdornment>
                            ),
                        }}
                    />
                </Box>

                <Box
                    display={'flex'}
                    flexDirection={'row'}
                    gap={2}
                >
                    {/* Tables */}
                    <SysPromptTable
                        sysPrompts={sysPrompts}
                        count={sysPromptCount}
                        currPage={sysPromptPage}
                        setCurrPage={setSysPromptPage}
                        selectedItem={sysPrompt}
                        setSelectedItem={setSelectedSysPrompt}
                    />
                    <ChatModelTable
                        chatModels={chatModels}
                        count={chatModelCount}
                        currPage={chatModelPage}
                        setCurrPage={setChatModelPage}
                        selectedItem={chatModel}
                        setSelectedItem={setSelectedChatModel}
                    />
                    <VecColTable
                        vectorCollections={vecCols}
                        count={vecColCount}
                        currPage={vecColPage}
                        setCurrPage={setVecColPage}
                        selectedItem={vecCol}
                        setSelectedItem={setSelectedVecCol}
                    />
                </Box>
            </Box>

            {/* SUBMIT */}
            <Button
                variant={'outlined'}
                onClick={handleSubmit}
            >
                submit
            </Button>

            {/* INFO SNACKBAR */}
            <Snackbar
                open={openSnackbar}
                message={snackbarMessage}
                onClose={() => setOpenSnackbar(false)}
                autoHideDuration={3000}
            />

        </Box>
    );
}
