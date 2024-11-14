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

import {API_URL} from "@/src/config";

export default function Page() {
    const router = useRouter();
    const [name, setName] = useState('');
    const [apiKey, setApiKey] = useState('');
    const [openSnackbar, setOpenSnackbar] = useState(false);
    const [snackbarMessage, setSnackbarMessage] = useState('');

    async function handleSubmit() {
        if (!name || !apiKey) {
            setSnackbarMessage("fulfill both fields 😡");
            setOpenSnackbar(true);
            return;
        }

        try {
            const response = await fetch(
                `${API_URL}/api-key/`,
                {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(
                        {
                            name: name,
                            api_key: apiKey
                        }
                    )
                }
            );
            if (response.status == 201) {
                router.push('/api-key');
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
            <Breadcrumbs>
                <Typography variant={'h6'}>
                    <MUILink
                        component={Link}
                        href={'/api-key'}
                        underline={'none'}
                    >
                        api-key
                    </MUILink>
                </Typography>
                <Typography variant={'h6'}>
                    add
                </Typography>
            </Breadcrumbs>

            <Divider sx={{width: '100%'}}/>

            <Box display={"flex"} gap={2}>
                <TextField
                    id={'name'}
                    variant={'standard'}
                    label={'name'}
                    value={name}
                    onChange={(e => {
                        setName(e.target.value)
                    })}
                />

                <TextField
                    id={'api-key'}
                    variant={'standard'}
                    label={'api key'}
                    value={apiKey}
                    onChange={(e) => {
                        setApiKey(e.target.value)
                    }}
                />
            </Box>

            <Button
                variant={'outlined'}
                onClick={handleSubmit}
            >
                submit
            </Button>

            {/* informing snackbar*/}
            <Snackbar
                open={openSnackbar}
                message={snackbarMessage}
                onClose={() => setOpenSnackbar(false)}
                autoHideDuration={3000}
            />
        </Box>
    );
}