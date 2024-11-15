'use client';

import {
    Box,
    Typography,
    Divider,
    Snackbar,
    Breadcrumbs,
    IconButton,
    Tooltip,
    Stack,
    Pagination
} from '@mui/material';
import AddIcon from '@mui/icons-material/Add';
import DeleteIcon from '@mui/icons-material/Delete';
import {useState, useEffect} from 'react';
import {useRouter} from 'next/navigation';
import OpenInNewIcon from '@mui/icons-material/OpenInNew';

import {API_URL, PAGE_LIMIT} from "@/src/constants";
import {ApiKeyResponseModel} from './models';
import {parseDateTime} from '@/src/utils';

export default function Page() {
    const router = useRouter();
    const [openSnackbar, setOpenSnackbar] = useState(false);
    const [snackbarMessage, setSnackbarMessage] = useState('');
    const [count, setCount] = useState(null);
    const [currPage, setCurrPage] = useState(1);
    const [items, setItems] = useState<ApiKeyResponseModel[]>([]);

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

    async function fetchItems() {
        const offset = (currPage - 1) * PAGE_LIMIT;

        try {
            const response = await fetch(
                `${API_URL}/api-key/?limit=${PAGE_LIMIT}&offset=${offset}`,
                {
                    method: 'GET'
                }
            );

            if (response.ok) {
                const data = await response.json();
                setItems(data);
            } else {
                setSnackbarMessage(`something went wrong 😢, status code: ${response.status}`);
                setOpenSnackbar(true);
            }
        } catch (error) {
            setSnackbarMessage(`something went wrong 😢, error: ${error.message}`);
            setOpenSnackbar(true);
        }
    }

    async function handleDelete(id: number) {
        try {
            const response = await fetch(
                `${API_URL}/api-key/${id}`,
                {
                    method: 'DELETE'
                }
            );

            if (response.status == 204) {
                setSnackbarMessage(`api key with the id: ${id} was successfully deleted 🥳`);
                setOpenSnackbar(true);
                await fetchApiKeyCount();
                await fetchItems();
            } else {
                setSnackbarMessage(`Something went wrong 😢, status code: ${response.status}`);
                setOpenSnackbar(true);
            }
        } catch (error) {
            setSnackbarMessage(`something went wrong 😢, error: ${error.message}`);
            setOpenSnackbar(true);
        }
    }

    useEffect(() => {
        fetchApiKeyCount();
        fetchItems();
    }, [currPage]);

    return (
        <Box
            display={'flex'}
            flexDirection={"column"}
            alignItems={'flex-start'}
            gap={2}
        >
            {/*TOP PANEL*/}
            <Box display={'flex'} width={'100%'}>
                <Breadcrumbs>
                    <Typography variant={'h6'}>
                        api-key
                    </Typography>
                </Breadcrumbs>
                <Tooltip title={'add new api-key credential'}>
                    <IconButton
                        onClick={() => router.push('/api-key/add')}
                        size={'small'}
                        sx={{ml: 'auto'}}
                    >
                        <AddIcon/>
                    </IconButton>
                </Tooltip>
            </Box>

            <Divider sx={{width: '100%'}}/>

            {/* CONTENT */}
            <Stack
                gap={2}
                divider={<Divider/>}
                width={'100%'}
            >
                {
                    items.map((item, _) => (
                        <Box
                            display={'flex'}
                        >
                            {/* DATE */}
                            <Typography color={'textSecondary'}>
                                {parseDateTime(item.datetime)}
                            </Typography>

                            {/* NAME */}
                            <Typography marginLeft={4}>{item.name}</Typography>

                            {/* ACTIONS */}
                            {/* DELETE */}
                            <Tooltip title={'delete api-key'}>
                                <IconButton
                                    sx={{ml: 'auto'}}
                                    size={'small'}
                                    onClick={() => handleDelete(item.id)}
                                >
                                    <DeleteIcon/>
                                </IconButton>
                            </Tooltip>

                            {/* OPEN */}
                            <Tooltip
                                title={'open api-key'}
                                onClick={() => router.push(`/api-key/${item.id}`)}
                            >
                                <IconButton size={'small'}>
                                    <OpenInNewIcon/>
                                </IconButton>
                            </Tooltip>
                        </Box>
                    ))
                }
            </Stack>

            {/* Pagination */}
            <Pagination
                count={Math.ceil(count / PAGE_LIMIT)}
                page={currPage}
                onChange={(_, page) => {
                    setCurrPage(page)
                }}
            />


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
