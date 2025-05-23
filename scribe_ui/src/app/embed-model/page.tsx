'use client';

import {useRouter} from "next/navigation";
import {useEffect, useState} from "react";
import {Box, Breadcrumbs, Divider, IconButton, Pagination, Snackbar, Stack, Tooltip, Typography} from "@mui/material";
import AddIcon from "@mui/icons-material/Add";
import DeleteIcon from "@mui/icons-material/Delete";
import OpenInNewIcon from "@mui/icons-material/OpenInNew";
import Link from 'next/link';
import {Link as MUILink} from '@mui/material';

import {parseDateTime} from "@/src/utils";
import {EmbeddingModelResponseModel} from './models';
import {API_URL, PAGE_LIMIT} from "@/src/constants";
import KeyIcon from '@mui/icons-material/Key';

export default function Page() {
    const router = useRouter();
    const [openSnackbar, setOpenSnackbar] = useState(false);
    const [snackbarMessage, setSnackbarMessage] = useState('');
    const [count, setCount] = useState(null);
    const [currPage, setCurrPage] = useState(1);
    const [items, setItems] = useState<EmbeddingModelResponseModel[]>([]);

    async function fetchCount() {
        try {
            const response = await fetch(
                `${API_URL}/embed-model/count`,
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
                `${API_URL}/embed-model/?limit=${PAGE_LIMIT}&offset=${offset}`,
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
                `${API_URL}/embed-model/${id}`,
                {
                    method: 'DELETE'
                }
            );

            if (response.status == 204) {
                setSnackbarMessage(`embedding model with the id: ${id} was successfully deleted 🥳`);
                setOpenSnackbar(true);
                await fetchCount();
                await fetchItems();
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
        fetchCount();
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
                        embed-model
                    </Typography>
                </Breadcrumbs>
                <Tooltip title={'add new embed-model'}>
                    <IconButton
                        onClick={() => router.push('/embed-model/add')}
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

                            {/*DEVICE */}
                            <Typography marginLeft={4}>{item.device}</Typography>

                            {/* API KEY */}
                            <KeyIcon sx={{marginLeft: 4}}/>
                            <Typography marginLeft={1}>
                                {/* if api_key_credential not null provide its name and link to it*/}
                                {
                                    !item.api_key_credential ? 'null' :
                                    <MUILink
                                        component={Link}
                                        href={`/api-key/${item.api_key_credential_id}`}
                                    >
                                        {item.api_key_credential.name}
                                    </MUILink>
                                }
                            </Typography>


                            {/* ACTIONS */}
                            {/* DELETE */}
                            <Tooltip title={'delete embed-model'}>
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
                                title={'open embed-model'}
                                onClick={() => router.push(`/embed-model/${item.id}`)}
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