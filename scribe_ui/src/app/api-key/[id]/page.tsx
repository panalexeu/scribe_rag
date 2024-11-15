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

import {ApiKeyPutModel, ApiKeyResponseModel} from "@/src/app/api-key/models";
import {API_URL} from "@/src/constants";


export default function Page() {
    const {id} = useParams();
    const router = useRouter();
    const [name, setName] = useState('');
    const [apiKey, setApiKey] = useState('');
    const [openSnackbar, setOpenSnackbar] = useState(false);
    const [snackbarMessage, setSnackbarMessage] = useState('');

    async function fetchApiKey() {
        try {
            const response = await fetch(
                `${API_URL}/api-key/${id}`,
                {
                    method: 'GET'
                }
            );

            if (response.status === 200) {
                const data: ApiKeyResponseModel = await response.json();
                setName(data.name);
                setApiKey(data.api_key);
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
        if (!name) {
            setSnackbarMessage("fulfill the name field 😡");
            setOpenSnackbar(true);
            return;
        }

        try {
            const apiKeyPostRequest = ApiKeyPutModel.parse({
                name: name
            })

            const response = await fetch(
                `${API_URL}/api-key/${id}`,
                {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(apiKeyPostRequest)
                }
            );
            if (response.status == 200) {
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

    useEffect(() => {
        fetchApiKey()
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
                        href={'/api-key'}
                        underline={'none'}
                    >
                        api-key
                    </MUILink>
                </Typography>
                <Typography variant={'h6'}>
                    {id}
                </Typography>
            </Breadcrumbs>

            {/* CONTENT */}
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
                    inputProps={{readOnly: true,}}
                    fullWidth={true}
                    multiline={true}
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