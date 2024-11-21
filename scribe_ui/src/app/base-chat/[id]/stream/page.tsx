'use client';

import {
    Breadcrumbs,
    Divider,
    Link as MUILink,
    Typography,
    Box,
    Snackbar,
    TextField,
    IconButton,
    Paper,
    Card,
    CardContent
} from "@mui/material";
import Link from "next/link";
import { useParams } from "next/navigation";
import { API_URL } from "@/src/constants";
import { useState, useEffect } from "react";
import PolylineIcon from "@mui/icons-material/Polyline";
import SmartToyIcon from "@mui/icons-material/SmartToy";
import DescriptionIcon from "@mui/icons-material/Description";
import SendIcon from '@mui/icons-material/Send';
import { VectorDocumentResponseModel } from "@/src/app/vec-col/models";
import axios from 'axios';

export default function Page() {
    const { id } = useParams();
    const [openSnackbar, setOpenSnackbar] = useState(false);
    const [snackbarMessage, setSnackbarMessage] = useState('');

    const [name, setName] = useState('');
    const [desc, setDesc] = useState('');
    const [sysPromptId, setSysPromptId] = useState<number>(null);
    const [chatModelId, setChatModelId] = useState<number>(null);
    const [vecColName, setVecColName] = useState<string>(null);

    const [contextDocs, setContextDocs] = useState<VectorDocumentResponseModel[]>([]);
    const [llmResponse, setLLMResponse] = useState<string>('');
    const [queryString, setQueryString] = useState('');

    async function fetchBaseChat() {
        try {
            const response = await fetch(`${API_URL}/base-chat/${id}`, {
                method: 'GET'
            });

            if (response.status === 200) {
                const data = await response.json();
                setName(data.name);
                setDesc(data.desc);
                setSysPromptId(data.system_prompt_id);
                setChatModelId(data.chat_model_id);
                setVecColName(data.vec_col_name);
            } else {
                setSnackbarMessage(`Something went wrong 😢, status code: ${response.status}`);
                setOpenSnackbar(true);
            }
        } catch (error) {
            setSnackbarMessage(`Something went wrong 😢, error: ${error.message}`);
            setOpenSnackbar(true);
        }
    }

    async function handleSubmit() {
        if (!queryString) {
            setSnackbarMessage(`Please provide a query string! 😠`);
            setOpenSnackbar(true);
            return;
        }
        try {
            const request = {
                query_string: queryString,
                doc_names: null,
                n_results: null
            };

            if (response.ok) {

            } else {
                setSnackbarMessage(`Something went wrong 😢, status code: ${response.status}`);
                setOpenSnackbar(true);
            }
        } catch (error) {
            setSnackbarMessage(`Something went wrong 😢, error: ${error.message}`);
            setOpenSnackbar(true);
        }
    }


    useEffect(() => {
        fetchBaseChat();
    }, []);

    return (
        <Box
            display={'flex'}
            flexDirection={"column"}
            alignItems={'flex-start'}
            gap={2}
        >
            {/* TOP PANEL */}
            <Breadcrumbs>
                <Typography variant={'h6'}>
                    <MUILink component={Link} href={'/base-chat'} underline={'none'}>
                        Base Chat
                    </MUILink>
                </Typography>
                <Typography variant={'h6'}>
                    <MUILink component={Link} href={`/base-chat/${id}`} underline={'none'}>
                        {id}
                    </MUILink>
                </Typography>
                <Typography variant={'h6'}>
                    Stream
                </Typography>
            </Breadcrumbs>

            <Divider sx={{ width: '100%' }} />

            {/* MAIN CONTENT */}
            <Box
                display={'flex'}
                flexDirection={'row'}
                sx={{ width: '100%' }}
                gap={2}
            >
                {/* INFO PANEL */}
                <Box
                    display={'flex'}
                    flexDirection={'column'}
                    gap={2}
                    width={'10%'}
                >
                    {/* NAME */}
                    <Box display={'flex'} alignItems={'center'} gap={1}>
                        <Typography variant={'body1'}>{name}</Typography>
                    </Box>

                    {/* VEC COL */}
                    <Box display={'flex'} alignItems={'center'} gap={1}>
                        <PolylineIcon />
                        <Typography variant={'body1'}>
                            {vecColName ? (
                                <MUILink component={Link} href={`/vec-col/${vecColName}`}>
                                    {vecColName}
                                </MUILink>
                            ) : 'null'}
                        </Typography>
                    </Box>

                    {/* CHAT MODEL */}
                    <Box display={'flex'} alignItems={'center'} gap={1}>
                        <SmartToyIcon />
                        <Typography variant={'body1'}>
                            {chatModelId ? (
                                <MUILink component={Link} href={`/chat-model/${chatModelId}`}>
                                    {chatModelId}
                                </MUILink>
                            ) : 'null'}
                        </Typography>
                    </Box>

                    {/* SYS PROMPT */}
                    <Box display={'flex'} alignItems={'center'} gap={1}>
                        <DescriptionIcon />
                        <Typography variant={'body1'}>
                            {sysPromptId ? (
                                <MUILink component={Link} href={`/sys-prompt/${sysPromptId}`}>
                                    {sysPromptId}
                                </MUILink>
                            ) : 'null'}
                        </Typography>
                    </Box>
                </Box>

                {/* LLM RESPONSE */}
                <Box width={'90%'} display={'flex'} flexDirection={'column'} gap={2}>
                    {/* RESPONSE AND METADATA */}
                    <Box display={'flex'} flexDirection={'row'} gap={2}>
                        {/* RESPONSE */}
                        <Paper variant={'outlined'} sx={{ height: '512px', overflowY: 'auto', width: '70%' }}>
                            <Typography variant="body1" sx={{ whiteSpace: 'pre-wrap', wordWrap: 'break-word' }}>
                                {llmResponse}
                            </Typography>
                        </Paper>

                        {/* CONTEXT DOCS */}
                        <Paper variant="outlined" sx={{ flex: 1, display: 'flex', flexDirection: 'column', width: '30%', overflow: 'hidden' }}>
                            <Box sx={{ padding: 1, overflowY: 'auto', maxHeight: '100%' }}>
                                {contextDocs.map((query, index) => (
                                    <Card key={index} variant="outlined" sx={{ padding: 1, overflowX: 'auto' }}>
                                        <CardContent>
                                            <Typography>ID: <strong>{query.id_}</strong></Typography>
                                            <Typography><strong>Distance:</strong> {query.distance}</Typography>
                                            <Typography><strong>Embedding:</strong> {query.embedding}</Typography>
                                            <Typography><strong>Document:</strong> {query.document}</Typography>
                                            <Typography><strong>Metadata:</strong>
                                                <pre style={{ whiteSpace: 'pre-wrap', wordWrap: 'break-word' }}>
                          {JSON.stringify(query.metadata, null, 2)}
                        </pre>
                                            </Typography>
                                        </CardContent>
                                    </Card>
                                ))}
                            </Box>
                        </Paper>
                    </Box>

                    {/* TEXT SUBMIT BOX */}
                    <TextField
                        fullWidth
                        variant="outlined"
                        placeholder="Type your message..."
                        multiline={true}
                        rows={3}
                        InputProps={{
                            endAdornment: (
                                <IconButton edge="end" onClick={handleSubmit} aria-label="send message">
                                    <SendIcon />
                                </IconButton>
                            )
                        }}
                        value={queryString}
                        onChange={(e) => setQueryString(e.target.value)}
                        onKeyDown={(e) => {
                            if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
                                e.preventDefault();
                                handleSubmit();
                            }
                        }}
                    />
                </Box>
            </Box>

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
