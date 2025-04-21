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
    IconButton, Card, CardContent, Paper
} from "@mui/material";
import DeleteIcon from '@mui/icons-material/Delete';
import Link from "next/link";
import {useParams} from "next/navigation";
import {useState, useEffect} from 'react';
import {API_URL} from "@/src/constants";
import SearchIcon from '@mui/icons-material/Search';
import { TextField, InputAdornment } from "@mui/material";

import {VectorDocumentResponseModel} from '@/src/app/vec-col/models';


export default function Page() {
    const {name} = useParams();
    const [openSnackbar, setOpenSnackbar] = useState(false);
    const [snackbarMessage, setSnackbarMessage] = useState('');

    const [nResults, setNResults] = useState<number>(1);
    const [query, setQuery] = useState('');
    const [docs, setDocs] = useState<string[]>([]);
    const [vecColDocsCount, setVecColDocsCount] = useState(0);
    const [queryResults, setQueryResults] = useState<VectorDocumentResponseModel[]>([]);

    async function fetchQuery() {
        if (!query) {
            setSnackbarMessage('provide search query! 😡');
            setOpenSnackbar(true);
            return;
        } else if (docs.length == 0) {
            setSnackbarMessage('vec-col is empty! 😡');
            setOpenSnackbar(true);
            return;
        } else if (nResults < 1) {
            setSnackbarMessage('number of results should be at least 1! 😡');
            setOpenSnackbar(true);
            return;
        }

        const request = {
            query_string: query,
            doc_names: docs,
            n_results: nResults
        }

        try {
            const response = await fetch(
                `${API_URL}/vec-doc/${name}/query`,
                {
                    method: 'post',
                    body: JSON.stringify(request),
                    headers: {
                        'Content-Type': 'application/json',
                    }
                }
            );

            if (response.status === 200) {
                const data = await response.json();
                setQueryResults(data);
            } else {
                setSnackbarMessage(`something went wrong 😢, status code: ${response.status}`);
                setOpenSnackbar(true);
            }
        } catch (error) {
            setSnackbarMessage(`something went wrong 😢, error: ${error.message}`);
            setOpenSnackbar(true);
        }
    }


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
                sx={{width: '75%'}}
                maxHeight={640}
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
                                    <IconButton onClick={() => fetchQuery()}>
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

                {/* QUERY SEARCH RESULTS */}
                { (queryResults.length > 0) && (
                    <Paper
                        sx={{
                            flex: 1,
                            display: 'flex',
                            flexDirection: 'column',
                            width: '100%',
                            overflow: 'hidden',
                        }}
                        variant="outlined"
                    >
                        <Box
                            sx={{
                                padding: 1,
                                overflowY: 'auto',
                                maxHeight: '100%',
                            }}
                        >
                            {queryResults.map((query, index) => (
                                <Card
                                    key={index}
                                    variant="outlined"
                                    sx={{
                                        padding: 1,
                                        overflowX: 'auto'
                                    }}
                                >
                                    <CardContent>
                                        <Typography>
                                            ID: <strong>{query.id_}</strong>
                                        </Typography>

                                        <Typography >
                                            <strong>Distance:</strong> {query.distance}
                                        </Typography>

                                        <Typography >
                                            <strong>Embedding:</strong> {query.embedding}
                                        </Typography>

                                        <Typography >
                                            <strong>Document:</strong> {query.document}
                                        </Typography>

                                        <Typography >
                                            <strong>Metadata:</strong>
                                            <pre style={{ whiteSpace: 'pre-wrap', wordWrap: 'break-word' }}>
                                                    {JSON.stringify(query.metadata, null, 2)}
                                                </pre>
                                        </Typography>
                                    </CardContent>
                                </Card>
                            ))}
                        </Box>
                    </Paper>
                    )}
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