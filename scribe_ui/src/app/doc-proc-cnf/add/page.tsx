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
    Switch,
    FormControlLabel,
    Autocomplete
} from '@mui/material';
import {useState} from 'react';
import {useRouter} from 'next/navigation';
import Link from 'next/link';

import {DocProcCnfPostModel, Postprocessor, ChunkingStrategy} from '../models';
import {API_URL} from "@/src/constants";


export default function Page() {
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

    async function handleSubmit() {
        if (!name) {
            setSnackbarMessage("fulfill the name field at least 😡");
            setOpenSnackbar(true);
            return;
        }

        try {
            const postRequest = DocProcCnfPostModel.parse({
                name: name,
                max_characters: !maxChars  ? null : Number(maxChars),
                new_after_n_chars: !newAfterNChars ? null : Number(newAfterNChars),
                overlap: !overlap ? null: Number(overlap),
                overlap_all: overlapAll,
                postprocessors: postprocessors,
                chunking_strategy: chunkingStrategy
            })

            const response = await fetch(
                `${API_URL}/doc-proc-cnf/`,
                {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(postRequest)
                }
            );
            if (response.status == 201) {
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
                    add
                </Typography>
            </Breadcrumbs>

            <Divider sx={{width: '100%'}}/>

            {/* MAIN CONTENT */}
            <Box>
                {/* NAME */}
                <TextField
                    id={'name'}
                    variant={'standard'}
                    label={'name'}
                    value={name}
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
                    fullWidth={true}
                    multiple
                    value={postprocessors}
                    options={postprocessorEnum}
                    onChange={(_, newValue: string[]) => setPostprocessors([...new Set(newValue)])}
                    renderInput={(params) => <TextField {...params} label="postprocessors" />}
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