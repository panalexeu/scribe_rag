'use client';

import {ApiKeyResponseModel} from "@/src/app/api-key/models";
import {
    Autocomplete,
    Box,
    Breadcrumbs, Button,
    Divider,
    Link as MUILink, Snackbar, Table, TableBody, TableCell,
    TableContainer, TableHead, TablePagination, TableRow,
    TextField,
    Typography,
    List,
    ListItem, ListItemText
} from "@mui/material";
import Link from "next/link";
import {useRouter} from 'next/navigation';

import {ChatModelPostModel, ChatModelName} from '../model';
import {useEffect, useState} from "react";
import {API_URL, TABLE_PAGE_LIMIT} from "@/src/constants";
import {parseDateTime} from "@/src/utils";

export default function Page() {
    const router = useRouter();
    const [openSnackbar, setOpenSnackbar] = useState(false);
    const [snackbarMessage, setSnackbarMessage] = useState('');
    const [count, setCount] = useState(null);
    const [currPage, setCurrPage] = useState(1);

    const [name, setName] = useState(null);
    const [apiKeyCredential, setApiKeyCredential] = useState<ApiKeyResponseModel>(null);
    const [temperature, setTemperature] = useState(null);
    const [topP, setTopP] = useState(null);
    const [baseURL, setBaseUrl] = useState(null);
    const [maxTokens, setMaxTokens] = useState(null);
    const [maxRetries, setMaxRetries] = useState(null);
    const [stopSequences, setStopSequences] = useState([]);
    const [stopSequence, setStopSequence] = useState(null);
    const [apiKeys, setApiKeys] = useState<ApiKeyResponseModel[]>([]);

    const chatModelNameEnum = Object.values(ChatModelName);


    async function fetchApiKeyCount() {
        try {
            const response = await fetch(
                `${API_URL}/api-key/count`,
                {
                    method: 'GET'
                }
            );

            if (response.status === 200) {
                const data = await response.json();
                setCount(data);
            } else {
                setSnackbarMessage(`something went wrong 😢, status code: ${response.status}`);
                setOpenSnackbar(true);
            }
        } catch (error) {
            setSnackbarMessage(`something went wrong 😢, error: ${error.message}`);
            setOpenSnackbar(true);
        }
    }

    async function fetchApiKeyItems() {
        const offset = (currPage - 1) * TABLE_PAGE_LIMIT;

        try {
            const response = await fetch(
                `${API_URL}/api-key/?limit=${TABLE_PAGE_LIMIT}&offset=${offset}`,
                {
                    method: 'GET'
                }
            );

            if (response.ok) {
                const data = await response.json();
                setApiKeys(data);
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
        if (!name || !apiKeyCredential) {
            setSnackbarMessage("fulfill name and api key fields at least 😡");
            setOpenSnackbar(true);
            return;
        }

        try {
            const postRequest = ChatModelPostModel.parse({
                name: name,
                api_key_credential_id: apiKeyCredential.id,
                temperature: !temperature ? null : Number(temperature),
                top_p: !topP ? null : Number(topP),
                base_url: baseURL,
                max_tokens: !maxTokens ? null : Number(maxTokens),
                max_retries: !maxRetries ? null : Number(maxRetries),
                stop_sequences: stopSequences
            })

            const response = await fetch(
                `${API_URL}/chat-model/`,
                {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(postRequest)
                }
            );
            if (response.status == 201) {
                router.push('/chat-model');
            } else {
                setSnackbarMessage(`smth went wrong 😢, status code: ${response.status}`);
                setOpenSnackbar(true);
            }
        } catch (error) {
            setSnackbarMessage(`smth went wrong 😢, error: ${error.message}`);
            setOpenSnackbar(true);
        }
    }

    useEffect(() => {
        fetchApiKeyCount()
        fetchApiKeyItems()
    }, [])

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
                        href={'/chat-model'}
                        underline={'none'}
                    >
                        chat-model
                    </MUILink>
                </Typography>
                <Typography variant={'h6'}>
                    add
                </Typography>
            </Breadcrumbs>

            <Divider sx={{width: '100%'}}/>

            {/* MAIN CONTENT */}
            <Box
                display={"flex"}
                gap={2}
                width={'50%'}
            >
                {/* CHAT MODEL NAME */}
                <Autocomplete
                    fullWidth={true}
                    value={name}
                    options={chatModelNameEnum}
                    onChange={(_, newValue) => setName(newValue)}
                    renderInput={(params) => <TextField {...params} label='chat-model name'/>}
                />

                {/* SELECTED API KEY */}
                <TextField
                    id={'api-key'}
                    variant={'outlined'}
                    label={'api key'}
                    value={!apiKeyCredential ? '' : apiKeyCredential.name}
                    inputProps={{readOnly: true,}}
                    fullWidth={true}
                    multiline={true}
                />
            </Box>

            {/* BASE URL AND TOP P*/}
            <Box
                display={"flex"}
                gap={2}
            >
                <TextField
                    id={'base-url'}
                    value={baseURL}
                    label={'base-url'}
                    variant={'standard'}
                    onChange={(e) => setBaseUrl(e.target.value)}
                />

                <TextField
                    id={'top-p'}
                    label={'top-p'}
                    variant={'standard'}
                    type={'number'}
                    value={topP}
                    onChange={(e) => setTopP(e.target.value)}
                />
            </Box>

            {/* MAX TOKENS AND MAX RETRIES */}
            <Box
                display={"flex"}
                gap={2}
            >
                <TextField
                    id={'max-tokens'}
                    label={'max-tokens'}
                    variant={'standard'}
                    type={'number'}
                    value={maxTokens}
                    onChange={(e) => setMaxTokens(e.target.value)}
                />

                <TextField
                    id={'max-retries'}
                    label={'max-retries'}
                    variant={'standard'}
                    type={'number'}
                    value={maxRetries}
                    onChange={(e) => setMaxRetries(e.target.value)}
                />
            </Box>

            {/* TEMPERATURE */}
            <TextField
                id={'temperature'}
                label={'temperature'}
                variant={'standard'}
                type={'number'}
                value={temperature}
                onChange={(e) => setTopP(e.target.value)}
            />


            <Divider sx={{width: '100%'}}/>

            {/* STOP SEQUENCES   */}
            <Box
                display={'flex'}
                gap={1}
            >
                <TextField
                    fullWidth={true}
                    variant={'standard'}
                    label={'stop-sequence'}
                    value={stopSequence}
                    onChange={(e) => setStopSequence(e.target.value)}
                />

                <Button
                    onClick={(event) => {
                        if (stopSequence.trim()) {
                            setStopSequences([...stopSequences, stopSequence]);
                            setStopSequence(null);
                        }
                    }}
                >
                    add
                </Button>
            </Box>

            <List
                sx={{
                    display: 'flex',
                    flexDirection: 'row'
                }}
            >
                {stopSequences.map((item, _) => (
                    <ListItem>
                        <ListItemText primary={item}/>
                    </ListItem>
                ))}

            </List>

            <Divider sx={{width: '100%'}}/>

            {/* API KEY TABLE*/}
            <Typography variant={'h6'}>
                api-keys
            </Typography>
            <TableContainer>
                <Table>
                    <TableHead>
                        <TableRow>
                            <TableCell>
                                datetime
                            </TableCell>
                            <TableCell>
                                name
                            </TableCell>
                            <TableCell>
                                api-key
                            </TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {/* TABLE CONTENT */}
                        {apiKeys.map((apiKey) => (
                            <TableRow
                                onClick={() => {
                                    setApiKeyCredential(apiKey)
                                }}
                                sx={{
                                    cursor: 'pointer',
                                    backgroundColor: apiKeyCredential && apiKeyCredential.id === apiKey.id ? 'rgba(0, 0, 0, 0.1)' : 'inherit',
                                }}
                            >
                                <TableCell>
                                    {parseDateTime(apiKey.datetime)}
                                </TableCell>
                                <TableCell>
                                    {apiKey.name}
                                </TableCell>
                                <TableCell>
                                    {apiKey.api_key}
                                </TableCell>
                            </TableRow>
                        ))

                        }
                    </TableBody>
                </Table>
            </TableContainer>
            <TablePagination
                page={currPage - 1}
                count={count}
                onPageChange={(_, newPage) => {
                    setCurrPage(newPage + 1)
                }}
                rowsPerPage={TABLE_PAGE_LIMIT}
                rowsPerPageOptions={[]}
            />

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