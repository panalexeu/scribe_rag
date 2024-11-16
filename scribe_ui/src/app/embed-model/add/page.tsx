'use client';

import {
    Box,
    Typography,
    Divider,
    TextField,
    Button,
    Snackbar,
    Breadcrumbs,
    Link as MUILink,
    Autocomplete,
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableHead,
    TablePagination,
    TableRow,
    Paper
} from '@mui/material';
import {useState, useEffect} from 'react';
import {useRouter} from 'next/navigation';
import Link from 'next/link';

import {parseDateTime} from "@/src/utils";
import {ApiKeyResponseModel} from "@/src/app/api-key/models";
import {EmbeddingModelPostModel, EmbeddingModelName} from '../models';
import {API_URL, TABLE_PAGE_LIMIT} from "@/src/constants";

export default function Page() {
    const router = useRouter();
    const [openSnackbar, setOpenSnackbar] = useState(false);
    const [snackbarMessage, setSnackbarMessage] = useState('');
    const [count, setCount] = useState(null);
    const [currPage, setCurrPage] = useState(1);


    const [name, setName] = useState(null);
    const [apiKeyCredential, setApiKeyCredential] = useState<ApiKeyResponseModel>(null);
    const [apiKeys, setApiKeys] = useState<ApiKeyResponseModel[]>([]);

    const embeddingModelNameEnum = Object.values(EmbeddingModelName);

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
            setSnackbarMessage("fulfill both fields 😡");
            setOpenSnackbar(true);
            return;
        }

        try {
            const postRequest = EmbeddingModelPostModel.parse({
                name: name,
                api_key_credential_id: apiKeyCredential.id
            })

            const response = await fetch(
                `${API_URL}/embed-model/`,
                {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(postRequest)
                }
            );
            if (response.status == 201) {
                router.push('/embed-model');
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
    }, [currPage])

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
                        href={'/embed-model'}
                        underline={'none'}
                    >
                        embed-model
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
                {/* EMBEDDING MODEL NAME */}
                <Autocomplete
                    fullWidth={true}
                    value={name}
                    options={embeddingModelNameEnum}
                    onChange={(_, newValue) => setName(newValue)}
                    renderInput={(params) => <TextField {...params} label='embed-model name'/>}
                />

                {/* SELECTED API KEY */}
                <TextField
                    id={'api-key'}
                    variant={'outlined'}
                    label={'api key'}
                    value={ !apiKeyCredential ? '' : apiKeyCredential.name  }
                    inputProps={{readOnly: true,}}
                    fullWidth={true}
                    multiline={true}
                />
            </Box>

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
                        { apiKeys.map((apiKey) => (
                            <TableRow
                                onClick={() => {setApiKeyCredential(apiKey)}}
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
                onPageChange={(_, newPage) => {setCurrPage(newPage + 1)}}
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