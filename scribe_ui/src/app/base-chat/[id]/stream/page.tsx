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
import ContentCopyIcon from '@mui/icons-material/ContentCopy';
import {useParams} from "next/navigation";
import {API_URL} from "@/src/constants";
import {useState, useEffect} from "react";
import PolylineIcon from "@mui/icons-material/Polyline";
import SmartToyIcon from "@mui/icons-material/SmartToy";
import {MuiMarkdown} from "mui-markdown";
import DescriptionIcon from "@mui/icons-material/Description";
import SendIcon from '@mui/icons-material/Send';
import {VectorCollectionResponseModel, VectorDocumentResponseModel} from "@/src/app/vec-col/models";
import {SysPromptResponseModel} from '@/src/app/sys-prompt/models';
import {ChatModelResponseModel} from "@/src/app/chat-model/models";
import {BaseChatResponseModel, BaseChatStreamModel} from '@/src/app/base-chat/models';


export default function Page() {
    const {id} = useParams();
    const [openSnackbar, setOpenSnackbar] = useState(false);
    const [snackbarMessage, setSnackbarMessage] = useState('');

    const [name, setName] = useState('');
    const [desc, setDesc] = useState('');
    const [sysPrompt, setSysPrompt] = useState<SysPromptResponseModel>(null);
    const [chatModel, setChatModel] = useState<ChatModelResponseModel>(null);
    const [vecCol, setVecCol] = useState<VectorCollectionResponseModel>(null);

    const [contextDocs, setContextDocs] = useState<VectorDocumentResponseModel[]>([]);
    const [llmResponse, setLLMResponse] = useState<string>('');
    const [queryString, setQueryString] = useState('');
    const [nResults, setNResults] = useState(1);

    async function fetchBaseChat() {
        try {
            const response = await fetch(`${API_URL}/base-chat/${id}`, {
                method: 'GET'
            });

            if (response.status === 200) {
                const data: BaseChatResponseModel = await response.json();
                setName(data.name);
                setDesc(data.desc);
                setSysPrompt(data.system_prompt);
                setChatModel(data.chat_model);
                setVecCol(data.vec_col);
            } else {
                setSnackbarMessage(`something went wrong 😢, status code: ${response.status}`);
                setOpenSnackbar(true);
            }
        } catch (error) {
            setSnackbarMessage(`something went wrong 😢, error: ${error.message}`);
            setOpenSnackbar(true);
        }
    }

    function decodeBase64Utf8(base64: string): string {
        const binaryStr = atob(base64);
        const bytes = Uint8Array.from(binaryStr, char => char.charCodeAt(0));
        const decoder = new TextDecoder('utf-8');
        return decoder.decode(bytes);
    }

    async function handleSubmit() {
        if (!queryString) {
            setSnackbarMessage(`please provide a query string! 😠`);
            setOpenSnackbar(true);
            return;
        }

        if (nResults < 0) {
            setSnackbarMessage('search results amount could not be negative! 😡');
            setOpenSnackbar(true);
            return;
        }

        // emptying previous related states
        setContextDocs([]);
        setLLMResponse('');
        setQueryString('');

        try {
            const request = BaseChatStreamModel.parse({
                query_string: queryString,
                n_results: nResults,
                doc_names: null,
            });

            const response = await fetch(
                `${API_URL}/base-chat/${id}/stream`,
                {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(request)
                }
            )

            // handling stream reading
            if (response.ok) {
                const reader = response.body.getReader();
                const decoder = new TextDecoder('utf-8');
                let buffer = '';

                while (true) {
                    const {value, done} = await reader.read();
                    if (done) break;

                    buffer += decoder.decode(value, {stream: true});

                    let lines = buffer.split('\n\n');
                    buffer = lines.pop();

                    for (let line of lines) {
                        if (line.trim() === '') continue;

                        const parsedLine = line.split('\n');
                        const eventType = parsedLine[0].split(' ')[1];
                        const data = parsedLine[1].split('data: ')[1];

                        switch (eventType) {
                            case ('docs'):
                                setContextDocs(JSON.parse(data));
                                break;
                            case ('response'):
                                const decodedData = decodeBase64Utf8(data);
                                setLLMResponse(prevState => prevState + decodedData);
                                break;
                        }
                    }
                }
            } else {
                setSnackbarMessage(`Something went wrong 😢, status code: ${response.status}`);
                setOpenSnackbar(true);
            }
        } catch (error) {
            setSnackbarMessage(`Something went wrong 😢, error: ${error.message}`);
            setOpenSnackbar(true);
        }
    }

    async function handleCopy() {
        navigator.clipboard.writeText(llmResponse).then(() => {
            setSnackbarMessage(`query string content was copied to the clipboard 🥳`);
            setOpenSnackbar(true);
        }).catch((err) => {
            setSnackbarMessage(`something went wrong while query string content to the clipboard 😢`);
            setOpenSnackbar(true);
        });
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
                        base-chat
                    </MUILink>
                </Typography>
                <Typography variant={'h6'}>
                    <MUILink component={Link} href={`/base-chat/${id}`} underline={'none'}>
                        {id}
                    </MUILink>
                </Typography>
                <Typography variant={'h6'}>
                    stream
                </Typography>
            </Breadcrumbs>

            <Divider sx={{width: '100%'}}/>

            {/* MAIN CONTENT */}
            <Box
                display={'flex'}
                flexDirection={'row'}
                sx={{width: '100%'}}
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

                    <Box display={'flex'} alignItems={'center'} gap={1}>
                        <Typography color={'textSecondary'} fontSize={'small'}>
                            {desc}
                        </Typography>
                    </Box>

                    {/* VEC COL */}
                    <Box display={'flex'} alignItems={'center'} gap={1}>
                        <PolylineIcon/>
                        <Typography variant={'body1'}>
                            {vecCol ? (
                                <MUILink component={Link} href={`/vec-col/${vecCol.id}`}>
                                    {vecCol.name}
                                </MUILink>
                            ) : 'null'}
                        </Typography>
                    </Box>

                    {/* CHAT MODEL */}
                    <Box display={'flex'} alignItems={'center'} gap={1}>
                        <SmartToyIcon/>
                        <Typography variant={'body1'}>
                            {chatModel ? (
                                <MUILink component={Link} href={`/chat-model/${chatModel.id}`}>
                                    {chatModel.name}
                                </MUILink>
                            ) : 'null'}
                        </Typography>
                    </Box>

                    {/* SYS PROMPT */}
                    <Box display={'flex'} alignItems={'center'} gap={1}>
                        <DescriptionIcon/>
                        <Typography variant={'body1'}>
                            {sysPrompt ? (
                                <MUILink component={Link} href={`/sys-prompt/${sysPrompt.id}`}>
                                    {sysPrompt.name}
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
                        <Paper
                            variant={'outlined'}
                            sx={{height: '512px', overflowY: 'auto', width: '70%', position: 'relative' }}
                        >
                            <MuiMarkdown>
                                {llmResponse}
                            </MuiMarkdown>
                            {/*<Typography variant="body1" sx={{whiteSpace: 'pre-wrap', wordWrap: 'break-word'}}>*/}
                            {/*    {llmResponse}*/}
                            {/*</Typography>*/}

                            {/* copy button*/}
                            <IconButton
                                onClick={handleCopy}
                                sx={{
                                    position: 'absolute',
                                    bottom: 8,
                                    right: 8,
                                    backgroundColor: 'rgba(0, 0, 0, 0.1)',
                                    '&:hover': {
                                        backgroundColor: 'rgba(0, 0, 0, 0.2)',
                                    },
                                }}
                            >
                                <ContentCopyIcon />
                            </IconButton>
                        </Paper>

                        {/* CONTEXT DOCS */}
                        <Paper variant="outlined" sx={{
                            flex: 1,
                            display: 'flex',
                            flexDirection: 'column',
                            width: '30%',
                            overflow: 'hidden',
                            height: '512px'
                        }}>
                            <Box sx={{padding: 1, overflowY: 'auto', maxHeight: '100%'}}>
                                {contextDocs.map((query, index) => (
                                    <Card key={index} variant="outlined" sx={{padding: 1, overflowX: 'auto'}}>
                                        <CardContent>
                                            <Typography><strong>ID:</strong> {query.id_}</Typography>
                                            <Typography><strong>Distance:</strong> {query.distance}</Typography>
                                            <Typography><strong>Embedding:</strong> {query.embedding}</Typography>
                                            <Typography><strong>Document:</strong> {query.document}</Typography>
                                            {/* Metadata*/}
                                            <Typography component={"pre"}>
                                                Metadata:
                                                {JSON.stringify(query.metadata, null,2)}
                                            </Typography>
                                        </CardContent>
                                    </Card>
                                ))}
                            </Box>
                        </Paper>
                    </Box>

                    {/* TEXT SUBMIT BOX */}
                    <Box
                        display={'flex'}
                        flexDirection={'row'}
                        gap={2}
                    >
                        <TextField
                            fullWidth
                            variant="outlined"
                            placeholder="Type your message..."
                            multiline={true}
                            rows={3}
                            InputProps={{
                                endAdornment: (
                                    <IconButton edge="end" onClick={handleSubmit} aria-label="send message">
                                        <SendIcon/>
                                    </IconButton>
                                )
                            }}
                            sx={{width: '70%'}}
                            value={queryString}
                            onChange={(e) => setQueryString(e.target.value)}
                            onKeyDown={(e) => {
                                if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
                                    e.preventDefault();
                                    handleSubmit();
                                }
                            }}
                        />

                        <TextField
                            type="number"
                            variant="outlined"
                            size="small"
                            label={'n-results'}
                            value={nResults}
                            onChange={(e) => setNResults(Number(e.target.value))}
                            sx={{width: '15%'}}
                        />
                    </Box>
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
