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
} from '@mui/material';
import AddIcon from '@mui/icons-material/Add';
import DeleteIcon from '@mui/icons-material/Delete';
import {useState, useEffect} from 'react';
import {useRouter} from 'next/navigation';
import {API_URL} from "@/src/config";
import OpenInNewIcon from '@mui/icons-material/OpenInNew';

export default function Page() {
    const router = useRouter();
    const [openSnackbar, setOpenSnackbar] = useState(false);
    const [snackbarMessage, setSnackbarMessage] = useState('');
    const [count, setCount] = useState(null);
    const [currPage, setCurrPage] = useState(1);
    const [items, setItems] = useState([]);
    const limit = 8;


    useEffect(() => {
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
            const offset = (currPage - 1) * limit;

            try {
                const response = await fetch(
                    `${API_URL}/api-key/?limit=${limit}&offset=${offset}`,
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

        fetchApiKeyCount();
        fetchItems();
    }, []);

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
            } else {
                setSnackbarMessage(`Something went wrong 😢, status code: ${response.status}`);
                setOpenSnackbar(true);
            }
        } catch (error) {
            setSnackbarMessage(`something went wrong 😢, error: ${error.message}`);
            setOpenSnackbar(true);
        }
    }

    return (
        <Box
            display={'flex'}
            flexDirection={"column"}
            alignItems={'flex-start'}
            gap={2}
        >
            {/*TOP PANEL*/}
            <Box display={'flex'} flexDirection={'row'} width={'100%'}>
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
                            <Typography>{item.name}</Typography>
                            <Tooltip title={'delete api-key'}>
                                <IconButton
                                    sx={{ml: 'auto'}}
                                    size={'small'}
                                    onClick={() => handleDelete(item.id)}
                                >
                                    <DeleteIcon/>
                                </IconButton>
                            </Tooltip>
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
