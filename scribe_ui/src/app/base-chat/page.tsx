'use client';

import {
    Box,
    Breadcrumbs,
    Divider,
    IconButton,
    Pagination,
    Snackbar,
    Tooltip,
    Typography,
    Stack, Link as MUILink
} from "@mui/material";
import AddIcon from "@mui/icons-material/Add";
import {useRouter} from 'next/navigation';
import {API_URL, PAGE_LIMIT} from "@/src/constants";
import {useEffect, useState} from "react";
import SmartToyIcon from '@mui/icons-material/SmartToy';
import Link from "next/link";
import DescriptionIcon from '@mui/icons-material/Description';
import DeleteIcon from "@mui/icons-material/Delete";
import OpenInNewIcon from "@mui/icons-material/OpenInNew";
import PolylineIcon from '@mui/icons-material/Polyline';

import {BaseChatResponseModel} from "@/src/app/base-chat/models";
import {parseDateTime} from "@/src/utils";


export default function Page() {
    const router = useRouter();
    const [openSnackbar, setOpenSnackbar] = useState(false);
    const [snackbarMessage, setSnackbarMessage] = useState('');
    const [count, setCount] = useState(null);
    const [currPage, setCurrPage] = useState(1);
    const [items, setItems] = useState<BaseChatResponseModel[]>([]);

    async function fetchCount() {
        try {
            const response = await fetch(
                `${API_URL}/base-chat/count`,
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
                `${API_URL}/base-chat/?limit=${PAGE_LIMIT}&offset=${offset}`,
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
                `${API_URL}/base-chat/${id}`,
                {
                    method: 'DELETE'
                }
            );

            if (response.status == 204) {
                setSnackbarMessage(`base chat with the id: ${id} was successfully deleted 🥳`);
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
                        base-chat
                    </Typography>
                </Breadcrumbs>
                <Tooltip title={'add new base-chat'}>
                    <IconButton
                        onClick={() => router.push('/base-chat/add')}
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
                            flexDirection={'column'}
                        >
                            {/* FIRST ROW   */}
                            <Box
                                display={'flex'}
                            >
                                {/* DATE */}
                                <Typography color={'textSecondary'}>
                                    {parseDateTime(item.datetime)}
                                </Typography>

                                {/* NAME */}
                                <Typography marginLeft={4}>{item.name}</Typography>

                                {/* VEC COL */}
                                <PolylineIcon sx={{marginLeft: 4}}/>
                                <Typography marginLeft={1}>
                                    {
                                        !item.vec_col_name ? 'null' :
                                            <MUILink
                                                component={Link}
                                                href={`/vec-col/${item.vec_col_name}`}
                                            >
                                                {item.vec_col_name}
                                            </MUILink>
                                    }
                                </Typography>

                                {/* CHAT MODEL */}
                                <SmartToyIcon sx={{marginLeft: 4}}/>
                                <Typography marginLeft={1}>
                                    {/* if api_key_credential not null provide its name and link to it*/}
                                    {
                                        !item.chat_model ? 'null' :
                                            <MUILink
                                                component={Link}
                                                href={`/chat-model/${item.chat_model_id}`}
                                            >
                                                {item.chat_model.name}
                                            </MUILink>
                                    }
                                </Typography>

                                {/* SYS PROMPT */}
                                <DescriptionIcon sx={{marginLeft: 4}}/>
                                <Typography marginLeft={1}>
                                    {
                                        !item.system_prompt ? 'null':
                                        <MUILink
                                            component={Link}
                                            href={`/sys-prompt/${item.system_prompt_id}`}
                                        >
                                            {item.system_prompt.name}
                                        </MUILink>
                                    }
                                </Typography>

                                {/* ACTIONS */}
                                {/* DELETE */}
                                <Tooltip title={'delete base-chat'}>
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
                                    title={'open base-chat'}
                                    onClick={() => router.push(`/base-chat/${item.id}`)}
                                >
                                    <IconButton size={'small'}>
                                        <OpenInNewIcon/>
                                    </IconButton>
                                </Tooltip>
                            </Box>

                            {/* SECOND ROW */}
                            <Box
                                display={'flex'}
                            >
                                {/* DESC*/}
                                <Typography color={'textSecondary'} fontSize={'small'}>
                                    {item.desc}
                                </Typography>
                            </Box>
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