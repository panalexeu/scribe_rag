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
    Autocomplete,
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableHead,
    TablePagination,
    TableRow,
} from '@mui/material';
import {useState, useEffect} from 'react';
import {useRouter} from 'next/navigation';
import Link from 'next/link';

import {parseDateTime} from "@/src/utils";
import {EmbeddingModelResponseModel} from '@/src/app/embed-model/models';
import {DistanceFunction, VectorCollectionPostModel} from "../models";
import {API_URL, PAGE_LIMIT, TABLE_PAGE_LIMIT} from "@/src/constants";

export default function Page() {
    const router = useRouter();
    const [openSnackbar, setOpenSnackbar] = useState(false);
    const [snackbarMessage, setSnackbarMessage] = useState('');
    const [count, setCount] = useState(null);
    const [currPage, setCurrPage] = useState(1);

    const [name, setName] = useState(null);
    const [distanceFunction, setDistanceFunction] = useState(null);
    const [embeddingModel, setEmbeddingModel] = useState<EmbeddingModelResponseModel>(null);
    const [embeddingModels, setEmbeddingModels] = useState<EmbeddingModelResponseModel[]>([]);

    const distanceFunctionEnum = Object.values(DistanceFunction);


    async function fetchEmbeddingModelCount() {
        try {
            const response = await fetch(
                `${API_URL}/embed-model/count`,
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

    async function fetchEmbeddingModels() {
        const offset = (currPage - 1) * PAGE_LIMIT;

        try {
            const response = await fetch(
                `${API_URL}/embed-model/?limit=${PAGE_LIMIT}&offset=${offset}`,
                {
                    method: 'GET'
                }
            );

            if (response.ok) {
                const data = await response.json();
                setEmbeddingModels(data);
            } else {
                setSnackbarMessage(`something went wrong 😢, status code: ${response.status}`);
                setOpenSnackbar(true);
            }
        } catch (error) {
            setSnackbarMessage(`something went wrong 😢, error: ${error.message}`);
            setOpenSnackbar(true);
        }
    }

    function validateInput(input: string): void {
        // length check
        if (input.length < 3 || input.length > 63) {
            throw new Error("Expected collection name contains 3-63 characters");
        // alphanumeric check
        } else if (!/^[a-zA-Z0-9._-]+$/.test(input)) {
            throw new Error("Expected collection contains only alphanumeric characters");
        // two dots check
        } else if (input.includes("..")) {
            throw new Error("Expected collection name doesn't contain two consecutive dots");
        }
    }

    async function handleSubmit() {
        if (!name || !distanceFunction || !embeddingModel) {
            setSnackbarMessage("fulfill all fields 😡");
            setOpenSnackbar(true);
            return;
        }

        try {
            const formatName = name.trim().replace(/\s+/g, '-');
            validateInput(formatName);

            const postRequest = VectorCollectionPostModel.parse({
                name: formatName,
                embedding_model_id: embeddingModel.id,
                distance_func: distanceFunction
            })

            const response = await fetch(
                `${API_URL}/vec-col/`,
                {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(postRequest)
                }
            );

            if (response.status == 201) {
                router.push('/vec-col');
            } else if (response.status == 400) {
                // TODO add collection name validation on UI side
                setSnackbarMessage(`irrelevant collection name was provided`); // check response detail field for more info
                setOpenSnackbar(true);
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
        fetchEmbeddingModelCount()
        fetchEmbeddingModels()
    }, [currPage])


    return(
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
                    add
                </Typography>
            </Breadcrumbs>

            <Divider sx={{width: '100%'}}/>



            {/* MAIN CONTENT */}
            {/* VEC-COL NAME */}
            <TextField
                id={'name'}
                label={'name'}
                value={name}
                onChange={(event) => setName(event.target.value)}
                variant={'standard'}
                sx={{width: '33%'}}
            />

            {/* DISTANCE FUNCTION AND EMBEDDING MODEL ID*/}
            <Box
                display={"flex"}
                gap={2}
                width={'50%'}
            >
                {/* DISTANCE FUNCTION */}
                <Autocomplete
                    fullWidth={true}
                    value={distanceFunction}
                    options={distanceFunctionEnum}
                    onChange={(_, newValue) => setDistanceFunction(newValue)}
                    renderInput={(params) => <TextField {...params} label='distance-func'/>}
                />

                {/* SELECTED EMBEDDING MODEL */}
                <TextField
                    id={'embed-model'}
                    variant={'outlined'}
                    label={'embed-model'}
                    value={ !embeddingModel? '' : embeddingModel.name  }
                    inputProps={{readOnly: true,}}
                    fullWidth={true}
                    multiline={true}
                />
            </Box>

            <Divider sx={{width: '100%'}}/>

            {/* EMBEDDING MODELS TABLE */}
            <Typography variant={'h6'}>
                embed-model
            </Typography>

            <TableContainer>
                <Table>
                    <TableHead>
                        <TableRow>
                            <TableCell>
                                datetime
                            </TableCell>
                            <TableCell>
                                name
                            </TableCell>
                            <TableCell>
                                device
                            </TableCell>
                            <TableCell>
                                api-key
                            </TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {/* TABLE CONTENT */}
                        { embeddingModels.map((embedModel) => (
                            <TableRow
                                onClick={() => {setEmbeddingModel(embedModel)}}
                                sx={{
                                    cursor: 'pointer',
                                    backgroundColor: embeddingModel && embeddingModel.id === embedModel.id ? 'rgba(0, 0, 0, 0.1)' : 'inherit',
                                }}
                            >
                                <TableCell>
                                    {parseDateTime(embedModel.datetime)}
                                </TableCell>
                                <TableCell>
                                    {embedModel.name}
                                </TableCell>
                                <TableCell>
                                    {embedModel.device}
                                </TableCell>
                                <TableCell>
                                    {
                                        !embedModel.api_key_credential ? 'null' :
                                            <MUILink
                                                component={Link}
                                                href={`/api-key/${embedModel.api_key_credential_id}`}
                                            >
                                                {embedModel.api_key_credential.name}
                                            </MUILink>
                                    }
                                </TableCell>
                            </TableRow>
                        ))

                        }
                    </TableBody>
                </Table>
            </TableContainer>

            <TablePagination
                page={currPage - 1}
                count={count}
                onPageChange={(_, newPage) => {setCurrPage(newPage + 1)}}
                rowsPerPage={TABLE_PAGE_LIMIT}
                rowsPerPageOptions={[]}
            />

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