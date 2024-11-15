'use client';

import {
    Box,
    Typography,
    Divider,
    TextField,
    Button,
    Snackbar,
    Breadcrumbs,
    Link as MUILink
} from '@mui/material';
import {useState} from 'react';
import {useRouter} from 'next/navigation';
import Link from 'next/link';

import {SysPromptPostModel} from '../models';
import {API_URL} from "@/src/constants";

export default function Page() {
    const router = useRouter();
    const [name, setName] = useState('');
    const [content, setContent] = useState('');
    const [openSnackbar, setOpenSnackbar] = useState(false);
    const [snackbarMessage, setSnackbarMessage] = useState('');

    async function handleSubmit() {
        if (!name || !content) {
            setSnackbarMessage("fulfill both fields 😡");
            setOpenSnackbar(true);
            return;
        }

        try {
            const postRequest = SysPromptPostModel.parse({
                name: name,
                content: content
            })

            const response = await fetch(
                `${API_URL}/sys-prompt/`,
                {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(postRequest)
                }
            );
            if (response.status == 201) {
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
                    add
                </Typography>
            </Breadcrumbs>

            <Divider sx={{width: '100%'}}/>

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