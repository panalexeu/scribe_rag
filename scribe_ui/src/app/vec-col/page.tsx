'use client';

import {useRouter} from "next/navigation";
import {useEffect, useState} from "react";
import DataArrayIcon from '@mui/icons-material/DataArray';
import {
    Box,
    Breadcrumbs,
    Divider,
    IconButton,
    Pagination,
    Snackbar,
    Stack,
    Tooltip,
    Typography
} from "@mui/material";
import Link from 'next/link';
import {Link as MUILink} from '@mui/material';
import AddIcon from "@mui/icons-material/Add";
import DeleteIcon from "@mui/icons-material/Delete";
import OpenInNewIcon from "@mui/icons-material/OpenInNew";

import {API_URL, PAGE_LIMIT} from "@/src/constants";
import {parseDateTime} from "@/src/utils";
import {VectorCollectionResponseModel} from "./models";


export default function Page() {
    const router = useRouter();
    const [openSnackbar, setOpenSnackbar] = useState(false);
    const [snackbarMessage, setSnackbarMessage] = useState('');
    const [count, setCount] = useState(null);
    const [currPage, setCurrPage] = useState(1);
    const [items, setItems] = useState<VectorCollectionResponseModel[]>([]);

    async function fetchCount() {
        try {
            const response = await fetch(
                `${API_URL}/vec-col/count`,
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
                `${API_URL}/vec-col/?limit=${PAGE_LIMIT}&offset=${offset}`,
                {
                    method: 'GET'
                }
            );

            if (response.ok) {
                const data = await response.json();
                console.log(data);
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

    async function handleDelete(name: string) {
        try {
            const response = await fetch(
                `${API_URL}/vec-col/${name}`,
                {
                    method: 'DELETE'
                }
            );

            if (response.status == 204) {
                setSnackbarMessage(`vector collection with the name: ${name} was successfully deleted 🥳`);
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
                        vec-col
                    </Typography>
                </Breadcrumbs>
                <Tooltip title={'add new vec-col'}>
                    <IconButton
                        onClick={() => router.push('/vec-col/add')}
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
                            {/* DATETIME */}
                            <Typography>
                                {parseDateTime(item.datetime)}
                            </Typography>

                            {/* NAME */}
                            <Typography marginLeft={4}>{item.name}</Typography>

                            {/* EMBEDDING MODEL*/}
                            <DataArrayIcon sx={{marginLeft: 4}} />
                            <Typography
                                marginLeft={1}
                            >
                                {
                                    !item.embedding_model ? 'null':
                                    <MUILink
                                        component={Link}
                                        href={`/embed-model/${item.embedding_model.id}`}
                                    >
                                        {item.embedding_model.name}
                                    </MUILink>
                                }
                            </Typography>

                            {/* ACTIONS */}
                            {/* DELETE */}
                            <Tooltip title={'delete vec-col'}>
                                <IconButton
                                    sx={{ml: 'auto'}}
                                    size={'small'}
                                    onClick={() => handleDelete(item.name)}
                                >
                                    <DeleteIcon/>
                                </IconButton>
                            </Tooltip>

                            {/* OPEN */}
                            <Tooltip
                                title={'open vec-col'}
                                onClick={() => router.push(`/vec-col/${item.name}`)}
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