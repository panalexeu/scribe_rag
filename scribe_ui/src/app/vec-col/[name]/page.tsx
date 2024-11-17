'use client';

import {
    Breadcrumbs,
    Divider,
    Link as MUILink,
    Snackbar,
    Typography,
    Box,
    TextField,
    Button,
    Dialog,
    DialogActions,
    DialogContent,
    DialogContentText,
    DialogTitle,
    DialogProps
} from "@mui/material";
import {useParams} from "next/navigation";
import {useState, useEffect} from "react";

import {VectorCollectionResponseModel} from '../models';
import {API_URL, TABLE_PAGE_LIMIT} from "@/src/constants";
import Link from "next/link";

export default function Page() {
    const {name} = useParams();
    const [openSnackbar, setOpenSnackbar] = useState(false);
    const [snackbarMessage, setSnackbarMessage] = useState('');
    const [metadataDialog, setMetadataDialog] = useState(false);
    const [scroll, setScroll] = useState<DialogProps['scroll']>('paper');

    const [vectorCollection, setVectorCollection] = useState<VectorCollectionResponseModel>(null)

    async function fetchVectorCollection() {
        try {
            const response = await fetch(
                `${API_URL}/vec-col/${name}`,
                {
                    method: 'GET'
                }
            );

            if (response.status === 200) {
                const data = await response.json();
                setVectorCollection(data);
            } else {
                setSnackbarMessage(`something went wrong 😢, status code: ${response.status}`);
                setOpenSnackbar(true);
            }
        } catch (error) {
            setSnackbarMessage(`something went wrong 😢, error: ${error.message}`);
            setOpenSnackbar(true);
        }
    }

    useEffect(() => {
        fetchVectorCollection()
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
                    {name}
                </Typography>
            </Breadcrumbs>

            <Divider sx={{width: '100%'}}/>

            {/* MAIN CONTENT */}
            {/* NAME AND METADATA DIALOG */}
            <Box
                display={"flex"}
                gap={2}
                width={'50%'}
            >
                {/* NAME */}
                <TextField
                    id={'name'}
                    label={'name'}
                    value={!vectorCollection ? '' : vectorCollection.name}
                    variant={'standard'}
                    inputProps={{readOnly: true,}}
                    sx={{width: '50%'}}
                />

                {/* METADATA DIALOG */}
                <Button
                    onClick={() => setMetadataDialog(true)}
                >
                    metadata
                </Button>

                <Dialog
                    open={metadataDialog}
                    onClose={() => setMetadataDialog(false)}
                    scroll={scroll}
                >
                    <DialogTitle>metadata</DialogTitle>
                    <DialogContent>
                        <DialogContentText>
                            {JSON.stringify(!vectorCollection ? null : vectorCollection.metadata)}
                        </DialogContentText>
                    </DialogContent>
                </Dialog>
            </Box>

            {/* SELECTED EMBEDDING FUNCTION */}
            <Box
                display={"flex"}
                gap={2}
                width={'50%'}
                flexDirection={'column'}
            >
                <TextField
                    id={'embed-func'}
                    variant={'outlined'}
                    label={'embed-func'}
                    value={!vectorCollection ? '' : vectorCollection.embedding_function}
                    inputProps={{readOnly: true,}}
                />
            </Box>

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