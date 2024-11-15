'use client';

import {
    Breadcrumbs,
    Link as MUILink,
    Typography,
    Box, Snackbar, TextField, Button
} from "@mui/material";
import Link from "next/link";
import {useParams} from 'next/navigation';
import {useState, useEffect} from 'react';
import {useRouter} from "next/navigation";

import {SysPromptPutModel, SysPromptResponseModel} from "../models";
import {API_URL} from "@/src/constants";


export default function Page() {
    const {id} = useParams();
    const router = useRouter();
    const [name, setName] = useState('');
    const [content, setContent] = useState('');
    const [openSnackbar, setOpenSnackbar] = useState(false);
    const [snackbarMessage, setSnackbarMessage] = useState('');

    async function fetchItem() {
        try {
            const response = await fetch(
                `${API_URL}/sys-prompt/${id}`,
                {
                    method: 'GET'
                }
            );

            if (response.status === 200) {
                const data: SysPromptResponseModel = await response.json();
                setName(data.name);
                setContent(data.content);
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
        if (!name || !content) {
            setSnackbarMessage("fulfill both fields! 😡");
            setOpenSnackbar(true);
            return;
        }

        try {
            const requestModel = SysPromptPutModel.parse({
                name: name,
                content: content
            })

            const response = await fetch(
                `${API_URL}/sys-prompt/${id}`,
                {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(requestModel)
                }
            );
            if (response.status == 200) {
                router.push('/sys-prompt');
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
        fetchItem()
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
                        href={'/sys-prompt'}
                        underline={'none'}
                    >
                        sys-prompt
                    </MUILink>
                </Typography>
                <Typography variant={'h6'}>
                    {id}
                </Typography>
            </Breadcrumbs>

            {/* MAIN CONTENT */}
            <Box
                display={"flex"}
                flexDirection={'column'}
                gap={2}
                width={'50%'}
            >
                {/* NAME */}
                <TextField
                    id={'name'}
                    variant={'standard'}
                    label={'name'}
                    value={name}
                    sx={{width: '50%'}}
                    onChange={(e => {setName(e.target.value)})}
                />

                {/* CONTENT */}
                <TextField
                    id={'sys-prompt'}
                    label={'sys-prompt'}
                    value={content}
                    multiline
                    rows={16}
                    variant={'outlined'}
                    onChange={(e) => {setContent(e.target.value)}}
                />

            </Box>

            {/* SUBMIT BUTTON */}
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