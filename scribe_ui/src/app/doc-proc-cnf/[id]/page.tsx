'use client';

import {
    Breadcrumbs,
    Link as MUILink,
    Typography,
    Box, Snackbar, TextField, Button, Divider, FormControlLabel, Switch, Autocomplete
} from "@mui/material";
import Link from "next/link";
import {useParams} from 'next/navigation';
import {useState, useEffect} from 'react';
import {useRouter} from "next/navigation";

import {ChunkingStrategy, DocProcCnfPutModel, DocProcCnfResponseModel, Postprocessor} from "../models";
import {API_URL} from "@/src/constants";


export default function Page() {
    const {id} = useParams();
    const router = useRouter();
    const [openSnackbar, setOpenSnackbar] = useState(false);
    const [snackbarMessage, setSnackbarMessage] = useState('');

    const [name, setName] = useState('');
    const [maxChars, setMaxChars] = useState(null);
    const [newAfterNChars, setNewAfterNChars] = useState(null);
    const [overlap, setOverlap] = useState(null);
    const [overlapAll, setOverlapAll] = useState(null);
    const [postprocessors, setPostprocessors] = useState([]);
    const [chunkingStrategy, setChunkingStrategy] = useState(null);

    const postprocessorEnum = Object.values(Postprocessor);
    const chunkingStrategyEnum = Object.values(ChunkingStrategy);

    async function fetchItem() {
        try {
            const response = await fetch(
                `${API_URL}/doc-proc-cnf/${id}`,
                {
                    method: 'GET'
                }
            );

            if (response.status === 200) {
                const data: DocProcCnfResponseModel = await response.json();
                setName(data.name);
                setMaxChars(data.max_characters);
                setNewAfterNChars(data.new_after_n_chars);
                setOverlap(data.overlap);
                setOverlapAll(data.overlap_all);
                setPostprocessors(JSON.parse(data.postprocessors) === null ? [] : JSON.parse(data.postprocessors));
                setChunkingStrategy(data.chunking_strategy);
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
        try {
            console.log(chunkingStrategy)
            const requestModel = DocProcCnfPutModel.parse({
                name: !name ? null: name,
                postprocessors: postprocessors.length === 0 ? null : JSON.stringify(postprocessors),
                chunking_strategy: !chunkingStrategy ? null: chunkingStrategy,
                overlap: !overlap ? null: Number(overlap),
                overlap_all: !overlapAll ? null: overlapAll,
                max_characters: !maxChars ? null: Number(maxChars),
                new_after_n_chars: !newAfterNChars ? null: Number(newAfterNChars),
            })

            console.log(requestModel);

            const response = await fetch(
                `${API_URL}/doc-proc-cnf/${id}`,
                {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(requestModel)
                }
            );
            if (response.status == 200) {
                router.push('/doc-proc-cnf');
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
                        href={'/doc-proc-cnf'}
                        underline={'none'}
                    >
                        doc-proc-cnf
                    </MUILink>
                </Typography>
                <Typography variant={'h6'}>
                    {id}
                </Typography>
            </Breadcrumbs>

            <Divider sx={{width: '100%'}}/>

            {/* MAIN CONTENT */}
            <Box>
                {/* NAME */}
                <TextField
                    id={'name'}
                    variant={'standard'}
                    value={name}
                    label={'name'}
                    onChange={(e) => setName(e.target.value)}
                />
            </Box>

            {/* ENUMS */}
            <Box
                display={"flex"}
                gap={2}
                width={'50%'}
            >
                <Autocomplete
                    fullWidth={true}
                    value={chunkingStrategy}
                    options={chunkingStrategyEnum}
                    renderInput={(params) => <TextField {...params} label="chunking-strategy"/>}
                    onChange={(_, newValue) => setChunkingStrategy(newValue)}

                />

                <Autocomplete
                    multiple
                    fullWidth={true}
                    value={postprocessors}
                    options={postprocessorEnum}
                    onChange={(_, newValue: string[]) => setPostprocessors([...new Set(newValue)])}
                    renderInput={(params) => <TextField {...params} label="postprocessors"/>}
                />
            </Box>

            {/* CONTENT THAT APPEARS AFTER CHUNKING STRATEGY CHOICE*/}
            { chunkingStrategy && <Box>
                <Divider/>

                <Typography color={'textSecondary'}>
                    chunking strategy params
                </Typography>


                {/* CHARS SETTINGS */}
                <Box
                    display={"flex"}
                    gap={2}
                >
                    <TextField
                        id={'max-chars'}
                        label={'max-chars'}
                        variant={'standard'}
                        type={'number'}
                        value={maxChars}
                        onChange={(e) => setMaxChars(e.target.value)}
                    />

                    <TextField
                        id={'new-after-n-chars'}
                        label={'new-after-n-chars'}
                        variant={'standard'}
                        type={'number'}
                        value={newAfterNChars}
                        onChange={(e) => setNewAfterNChars(e.target.value)}
                    />
                </Box>

                {/* OVERLAP SETTINGS*/}
                <Box
                    display={"flex"}
                    gap={2}
                >
                    <TextField
                        id={'overlap'}
                        label={'overlap'}
                        variant={'standard'}
                        type={'number'}
                        value={overlap}
                        onChange={(e) => setOverlap(e.target.value)}
                    />

                    <FormControlLabel
                        control={
                            <Switch
                                checked={overlapAll}
                                onChange={(e) => setOverlapAll(e.target.checked)}
                            />
                        }
                        label="overlap-all"
                    />
                </Box>
            </Box> }

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