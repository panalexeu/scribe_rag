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
} from '@mui/material';
import {useState} from 'react';
import {useRouter} from 'next/navigation';
import Link from 'next/link';

import {SemDocProcCnfPostModel} from '../models';
import {API_URL} from "@/src/constants";


export default function Page() {
    const router = useRouter();
    const [openSnackbar, setOpenSnackbar] = useState(false);
    const [snackbarMessage, setSnackbarMessage] = useState('');

    const [name, setName] = useState('');
    const [thresh, setThresh] = useState(null);
    const [maxChunkSize, setMaxChunkSize] = useState(null);

    async function handleSubmit() {
        if (!name || !thresh || !maxChunkSize) {
            setSnackbarMessage("fulfill all fields 😡");
            setOpenSnackbar(true);
            return;
        }

        try {
            const postRequest = SemDocProcCnfPostModel.parse({
                name: name,
                thresh: Number(thresh),
                max_chunk_size: Number(maxChunkSize)
            })

            const response = await fetch(
                `${API_URL}/sem-doc-proc-cnf/`,
                {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(postRequest)
                }
            );
            if (response.status == 201) {
                router.push('/sem-doc-proc-cnf');
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
                        href={'/sem-doc-proc-cnf'}
                        underline={'none'}
                    >
                        sem-doc-proc-cnf
                    </MUILink>
                </Typography>
                <Typography variant={'h6'}>
                    add
                </Typography>
            </Breadcrumbs>

            <Divider sx={{width: '100%'}}/>

            {/* MAIN CONTENT */}
            <Box
                sx={{
                    display: 'flex',
                    flexDirection: 'row',
                    gap: 2
                }}
            >
                {/* NAME */}
                <TextField
                    id={'name'}
                    variant={'standard'}
                    label={'name'}
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    sx={{ flex: 3}}
                />

                {/* THRESH */}
                <TextField
                    id={'thresh'}
                    label={'thresh'}
                    variant={'standard'}
                    type={'number'}
                    value={thresh}
                    onChange={(e) => setThresh(e.target.value)}
                    sx={{ flex: 1}}
                />

                {/* MAX_CHUNK_SIZE */}
                <TextField
                    id={'max-chunk-size'}
                    label={'max-chunk-size'}
                    variant={'standard'}
                    type={'number'}
                    value={maxChunkSize}
                    onChange={(e) => setMaxChunkSize(e.target.value)}
                    sx={{ flex: 1}}
                />
            </Box>

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