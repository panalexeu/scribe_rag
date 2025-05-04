'use client';

import {useRouter} from "next/navigation";
import {useEffect, useState} from "react";
import {Box, Breadcrumbs, Divider, IconButton, Pagination, Snackbar, Stack, Tooltip, Typography} from "@mui/material";
import AddIcon from "@mui/icons-material/Add";
import DeleteIcon from "@mui/icons-material/Delete";
import OpenInNewIcon from "@mui/icons-material/OpenInNew";

import {parseDateTime} from "@/src/utils";
import {SemDocProcCnfResponseModel} from './models';
import {API_URL, PAGE_LIMIT} from "@/src/constants";

export default function Page() {
    const router = useRouter();
    const [openSnackbar, setOpenSnackbar] = useState(false);
    const [snackbarMessage, setSnackbarMessage] = useState('');
    const [count, setCount] = useState(null);
    const [currPage, setCurrPage] = useState(1);
    const [items, setItems] = useState<SemDocProcCnfResponseModel[]>([]);

    async function fetchCount() {
        try {
            const response = await fetch(
                `${API_URL}/sem-doc-proc-cnf/count`,
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
                `${API_URL}/sem-doc-proc-cnf/?limit=${PAGE_LIMIT}&offset=${offset}`,
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
                `${API_URL}/sem-doc-proc-cnf/${id}`,
                {
                    method: 'DELETE'
                }
            );

            if (response.status == 204) {
                setSnackbarMessage(`semantic doc processing cnf with the id: ${id} was successfully deleted 🥳`);
                setOpenSnackbar(true);
                await fetchCount();
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
                        sem-doc-proc-cnf
                    </Typography>
                </Breadcrumbs>
                <Tooltip title={'add new sem-doc-proc-cnf'}>
                    <IconButton
                        onClick={() => router.push('/sem-doc-proc-cnf/add')}
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
                            <Tooltip title={'delete sem-doc-proc-cnf'}>
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
                                title={'open sem-doc-proc-cnf'}
                                onClick={() => router.push(`/sem-doc-proc-cnf/${item.id}`)}
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