'use client';

import {
    Breadcrumbs,
    Link as MUILink,
    Typography,
    Box,
    Divider,
    Snackbar,
    List,
    ListItem,
    ListItemText,
    IconButton
} from "@mui/material";
import DeleteIcon from '@mui/icons-material/Delete';
import Link from "next/link";
import {useParams} from "next/navigation";
import {useState, useEffect} from 'react';
import {API_URL} from "@/src/constants";
import SearchIcon from '@mui/icons-material/Search'; // Import the Search icon
import { TextField, InputAdornment } from "@mui/material"; // Import required MUI components


export default function Page() {
    const {name} = useParams();
    const [openSnackbar, setOpenSnackbar] = useState(false);
    const [snackbarMessage, setSnackbarMessage] = useState('');

    const [nResults, setNResults] = useState<number>(1);
    const [query, setQuery] = useState('');
    const [docs, setDocs] = useState<string[]>([]);
    const [vecColDocsCount, setVecColDocsCount] = useState(0);

    async function fetchVectorDocsCount() {
        try {
            const response = await fetch(
                `${API_URL}/vec-doc/${name}/count`,
                {
                    method: 'GET'
                }
            );

            if (response.status === 200) {
                const data = await response.json();
                setVecColDocsCount(data);
            } else {
                setSnackbarMessage(`something went wrong 😢, status code: ${response.status}`);
                setOpenSnackbar(true);
            }
        } catch (error) {
            setSnackbarMessage(`something went wrong 😢, error: ${error.message}`);
            setOpenSnackbar(true);
        }
    }

    async function fetchDocs() {
        try {
            const response = await fetch(
                `${API_URL}/vec-doc/${name}/docs`,
                {
                    method: 'GET'
                }
            );

            if (response.status === 200) {
                const data = await response.json();
                setDocs(data);
            } else {
                setSnackbarMessage(`something went wrong 😢, status code: ${response.status}`);
                setOpenSnackbar(true);
            }
        } catch (error) {
            setSnackbarMessage(`something went wrong 😢, error: ${error.message}`);
            setOpenSnackbar(true);
        }
    }

    async function handleDocRemove(index) {
        const docToRemove = docs[index];
        const request = {
            doc_name: docToRemove
        }

        try {
            const response = await fetch(
                `${API_URL}/vec-doc/${name}`,
                {
                    method: 'DELETE',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(request)
                }
            );

            if (response.status === 204) {
                setSnackbarMessage(`document with the name: ${docToRemove} was successfully removed from the vec-col: ${name} 🥳`);
                setOpenSnackbar(true);
                await fetchDocs();
                await fetchVectorDocsCount();
            } else {
                setSnackbarMessage(`something went wrong 😢, status code: ${response.status}`);
                setOpenSnackbar(true);
            }
        } catch (error) {
            setSnackbarMessage(`something went wrong 😢, error: ${error.message}`);
            setOpenSnackbar(true);
        } finally {
        }
    }

    useEffect(() => {
        fetchDocs();
        fetchVectorDocsCount();
    }, []);

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
                        href={'/vec-col'}
                        underline={'none'}
                    >
                        vec-col
                    </MUILink>
                </Typography>

                <Typography variant={'h6'}>
                    <MUILink
                        component={Link}
                        href={`/vec-col/${name}`}
                        underline={'none'}
                    >
                        {name}
                    </MUILink>
                </Typography>

                <Typography variant={'h6'}>
                    explore
                </Typography>

            </Breadcrumbs>

            <Divider sx={{width: '100%'}}/>

            {/* MAIN CONTENT */}
            {/* QUERY PLAYGROUND */}
            <Box
                display={'flex'}
                flexDirection={'column'}
                alignItems={'flex-start'}
                gap={1}
                sx={{width: '50%'}}
            >
                <Typography>
                    query-playground
                </Typography>

                <Box
                    display={'flex'}
                    flexDirection={'row'}
                    gap={1}
                >

                    <TextField
                        variant="outlined"
                        size="small"
                        placeholder="Search..."
                        value={query}
                        onChange={(e) => setQuery(e.target.value)}
                        sx={{width: '85%'}}
                        InputProps={{
                            endAdornment: (
                                <InputAdornment position="end">
                                    <IconButton onClick={() => console.log("Searching for:", query)}>
                                        <SearchIcon />
                                    </IconButton>
                                </InputAdornment>
                            )
                        }}
                    />

                    <TextField
                        type="number"
                        variant="outlined"
                        size="small"
                        label={'n-results'}
                        value={nResults}
                        onChange={(e) => setNResults(Number(e.target.value))}
                        sx={{width: '15%'}}
                    />
                </Box>
            </Box>

            <Divider sx={{width: '100%'}}/>

            {/* DOCUMENTS LIST */}
            <Box
                display={'flex'}
                flexDirection={'column'}
            >
                <Box
                    display={'flex'}
                    flexDirection={'column'}
                    gap={2}
                >
                    <Typography>
                        docs: {vecColDocsCount}
                    </Typography>

                    {docs.length > 0 && (
                        <Box
                            sx={{border: '1px dashed grey', borderRadius: '4px'}}
                            display={'flex'}
                            flexDirection={'column'}
                        >
                            <List>
                                {
                                    docs.map((doc, index) => (
                                        <ListItem key={index}>
                                            <ListItemText>
                                                {doc}
                                            </ListItemText>

                                            <IconButton
                                                sx={{ml: 1}}
                                                color="error"
                                                size="small"
                                                onClick={() => handleDocRemove(index)}
                                            >
                                                <DeleteIcon/>
                                            </IconButton>
                                        </ListItem>
                                    ))
                                }
                            </List>


                        </Box>
                    )}
                </Box>
            </Box>

            {/* INFO SNACKBAR */}
            <Snackbar
                open={openSnackbar}
                message={snackbarMessage}
                onClose={() => setOpenSnackbar(false)}
                autoHideDuration={6000}
            />
        </Box>
    );
}