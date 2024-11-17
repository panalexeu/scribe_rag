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
    DialogContent,
    DialogContentText,
    DialogTitle,
    DialogProps, List, ListItem, ListItemText, ListItemIcon,
    IconButton,
    CircularProgress
} from "@mui/material";
import LinkIcon from '@mui/icons-material/Link';
import DeleteIcon from '@mui/icons-material/Delete';
import InsertDriveFileIcon from '@mui/icons-material/InsertDriveFile';
import {useParams} from "next/navigation";
import FileUploadIcon from '@mui/icons-material/FileUpload';
import {useState, useEffect} from "react";

import {VectorCollectionResponseModel} from '../models';
import {API_URL, TABLE_PAGE_LIMIT} from "@/src/constants";
import Link from "next/link";

export default function Page() {
    const {name} = useParams();
    const [openSnackbar, setOpenSnackbar] = useState(false);
    const [snackbarMessage, setSnackbarMessage] = useState('');
    const [urlDialog, setUrlDialog] = useState(false);
    const [scroll, setScroll] = useState<DialogProps['scroll']>('paper');

    const [vectorCollection, setVectorCollection] = useState<VectorCollectionResponseModel>(null)

    const [selectedUrls, setSelectedUrls] = useState([]);
    const [selectedFiles, setSelectedFiles] = useState([]);
    const [uploading, setUploading] = useState(false);

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

    // docs related functions
    const handleFileChange = (event) => {
        const files = Array.from(event.target.files);
        setSelectedFiles((prevFiles) => [...prevFiles, ...files])
    }

    const handleRemoveFile = (index) => {
        setSelectedFiles((prevFiles) => prevFiles.filter((_, i) => i !== index));
    }

    const handleRemoveUrl = (index) => {
        setSelectedUrls((prevUrls) => prevUrls.filter((_, i) => i !== index));
    }

    const handleUpload = async () => {
        if (selectedFiles.length === 0) {
            setSnackbarMessage(`add files to upload!`);
            setOpenSnackbar(true);
            return;
        }

        setUploading(true);

        // handling form
        const formData = new FormData();
        selectedFiles.forEach((file) => formData.append('files', file));
        // mocks
        formData.set('doc_processing_cnf_id', '1')

        // sending request
        try {
            for (let [key, value] of formData.entries()) {
                console.log(`${key}: ${value}`);
            }
            const response = await fetch(
                `${API_URL}/vec-doc/${name}`,
                {
                    method: 'POST',
                    body: formData
                }
            );

            if (response.status === 201) {
                setSnackbarMessage(`docs were successfully uploaded 🥳`);
                setOpenSnackbar(true);
            } else {
                setSnackbarMessage(`something went wrong 😢, status code: ${response.status}`);
                setOpenSnackbar(true);
            }
        } catch (error) {
            setSnackbarMessage(`something went wrong 😢, error: ${error.message}`);
            setOpenSnackbar(true);
        } finally {
            setUploading(false);
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

                {/* METADATA */}
                <TextField
                    id={'metadata'}
                    variant={'outlined'}
                    label={'metadata'}
                    value={JSON.stringify(!vectorCollection ? null : vectorCollection.metadata)}
                    inputProps={{readOnly: true,}}
                    sx={{width: '50%'}}
                />
            </Box>

            {/* EMBEDDING FUNCTION */}
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

            <Divider sx={{width: '100%'}}/>

            {/* UPLOAD A DOCUMENT */}
            <Box
                display={'flex'}
                gap={2}
            >
                <Typography>
                    upload file/url docs to vec-col
                </Typography>

                {/* URLS BUTTON*/}
                <Button
                    onClick={() => setUrlDialog(true)}
                >
                    add urls
                </Button>

                <Dialog
                    open={urlDialog}
                >
                </Dialog>


                {/* FILES BUTTON */}
                <Button
                    component={'label'}
                >
                    select files
                    <input
                        type={'file'}
                        multiple
                        hidden
                        onChange={handleFileChange}
                    />
                </Button>
            </Box>

            {/* UPLOADED URLS/FILES BOX */}
            {selectedFiles.length > 0 && (
                <Box
                    sx={{border: '1px dashed grey', borderRadius: '4px'}}
                    display={'flex'}
                    flexDirection={'column'}
                >
                    {/* SELECTED FILES AND URLS LIST */}
                    <List>
                        {/* FILES */}
                        {selectedFiles.map((file, index) => (
                                <ListItem key={index}>
                                    <ListItemIcon>
                                        <InsertDriveFileIcon/>
                                    </ListItemIcon>

                                    <ListItemText
                                        primary={file.name}
                                        secondary={`${(file.size / 1024).toFixed(2)} KB`}
                                    />
                                    <IconButton
                                        sx={{ml: 1}}
                                        color="error"
                                        size="small"
                                        onClick={() => handleRemoveFile(index)}
                                    >
                                        <DeleteIcon/>
                                    </IconButton>
                                </ListItem>
                            )
                        )}

                        <Divider/>

                        {/* URLS */}
                        {selectedUrls.map((url, index) => (
                            <ListItem key={index}>
                                <ListItemIcon>
                                    <LinkIcon/>
                                </ListItemIcon>

                                <ListItemText
                                    primary={url}
                                />
                                <IconButton
                                    sx={{ml: 1}}
                                    color="error"
                                    size="small"
                                    onClick={() => handleRemoveUrl(index)}
                                >
                                    <DeleteIcon/>
                                </IconButton>
                            </ListItem>
                        ))}

                    </List>

                    {/* UPLOAD BUTTON */}
                    <Button
                        variant={'contained'}
                        startIcon={<FileUploadIcon/>}
                        onClick={handleUpload}
                        disabled={uploading}
                    >
                        {uploading ? <CircularProgress/> : 'upload docs'}
                    </Button>
                </Box>
            )}

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