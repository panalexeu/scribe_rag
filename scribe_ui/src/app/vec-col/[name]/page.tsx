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
    DialogActions, CardContent, Card,
    Paper,
    CircularProgress, TableContainer, Table, TableHead, TableRow, TableCell, TableBody, TablePagination, Tooltip,
} from "@mui/material";
import OpenInNewIcon from '@mui/icons-material/OpenInNew';
import LinkIcon from '@mui/icons-material/Link';
import DeleteIcon from '@mui/icons-material/Delete';
import InsertDriveFileIcon from '@mui/icons-material/InsertDriveFile';
import {useParams} from "next/navigation";
import FileUploadIcon from '@mui/icons-material/FileUpload';
import {useState, useEffect} from "react";

import {DocProcCnfResponseModel} from '@/src/app/doc-proc-cnf/models';
import {VectorCollectionResponseModel, VectorDocumentResponseModel} from '../models';
import {API_URL, TABLE_PAGE_LIMIT} from "@/src/constants";
import Link from "next/link";
import {parseDateTime} from "@/src/utils";

export default function Page() {
    const {name} = useParams();
    const [openSnackbar, setOpenSnackbar] = useState(false);
    const [snackbarMessage, setSnackbarMessage] = useState('');
    const [urlDialog, setUrlDialog] = useState(false);
    const [scroll, setScroll] = useState<DialogProps['scroll']>('paper');
    const [count, setCount] = useState(null);
    const [currPage, setCurrPage] = useState(1);

    const [vectorCollection, setVectorCollection] = useState<VectorCollectionResponseModel>(null)

    const [selectedUrlInput, setSelectedUrlInput] = useState(null);
    const [selectedUrls, setSelectedUrls] = useState([]);
    const [selectedFiles, setSelectedFiles] = useState([]);
    const [uploading, setUploading] = useState(false);
    const [docProcConfigs, setDocProcConfigs] = useState<DocProcCnfResponseModel[]>([]);
    const [docProcessingConfig, setDocProcessingConfig] = useState(null);
    const [vecColPeek, setVecColPeek] = useState<VectorDocumentResponseModel[]>([]);
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

    async function fetchVectorCollectionPeek() {
        try {
            const response = await fetch(
                `${API_URL}/vec-doc/${name}/peek`,
                {
                    method: 'GET'
                }
            );

            if (response.status === 200) {
                const data = await response.json();
                setVecColPeek(data);
            } else {
                setSnackbarMessage(`something went wrong 😢, status code: ${response.status}`);
                setOpenSnackbar(true);
            }
        } catch (error) {
            setSnackbarMessage(`something went wrong 😢, error: ${error.message}`);
            setOpenSnackbar(true);
        }
    }

    async function fetchDocProcCnfCount() {
        try {
            const response = await fetch(
                `${API_URL}/doc-proc-cnf/count`,
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

    async function fetchDocProcCnfItems() {
        const offset = (currPage - 1) * TABLE_PAGE_LIMIT;

        try {
            const response = await fetch(
                `${API_URL}/doc-proc-cnf/?limit=${TABLE_PAGE_LIMIT}&offset=${offset}`,
                {
                    method: 'GET'
                }
            );

            if (response.ok) {
                const data = await response.json();
                setDocProcConfigs(data);
            } else {
                setSnackbarMessage(`something went wrong 😢, status code: ${response.status}`);
                setOpenSnackbar(true);
            }
        } catch (error) {
            setSnackbarMessage(`something went wrong 😢, error: ${error.message}`);
            setOpenSnackbar(true);
        }
    }

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
        if (!docProcessingConfig) {
            setSnackbarMessage(`provide doc-proc-cnf! 😡`);
            setOpenSnackbar(true);
            return;
        }

        if (selectedFiles.length === 0 && selectedUrls.length == 0) {
            setSnackbarMessage(`add files/urls to upload 😡`);
            setOpenSnackbar(true);
            return;
        }

        setUploading(true);

        // handling form
        const formData = new FormData();
        if (selectedFiles.length > 0) selectedFiles.forEach((file) => formData.append('files', file));
        if (selectedUrls.length > 0) selectedUrls.forEach((url) => formData.append('urls', url));
        formData.set('doc_processing_cnf_id', docProcessingConfig.id)

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

                // emptying selected files, and refetching the peek
                setSelectedUrls([]);
                setSelectedFiles([]);
                fetchVectorCollectionPeek();
                fetchVectorDocsCount();
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
        fetchVectorCollectionPeek()
        fetchVectorDocsCount()
    }, []);

    useEffect(() => {
        fetchDocProcCnfCount()
        fetchDocProcCnfItems()
    }, [currPage])

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

            {/* DOC PROC CNF AND DATA PEEK*/}
            <Box
                display={'flex'}
                flexDirection={'row'}
                gap={2}
                sx={{width: '100%'}}
            >
                {/* DOC PROC CNF */}
                <Box
                    sx={{width: '50%'}}
                >
                    <Box
                        display={'flex'}
                        gap={2}
                    >
                        <Typography>
                            doc-proc-cnf
                        </Typography>

                        <TextField
                            id={'doc-proc-cnf'}
                            variant={'outlined'}
                            label={'doc-proc-cnf'}
                            value={!docProcessingConfig ? '' : docProcessingConfig.name}
                            inputProps={{readOnly: true,}}
                        />
                    </Box>

                    {/* TABLE */}
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
                                        link
                                    </TableCell>
                                </TableRow>
                            </TableHead>
                            <TableBody>
                                {/* TABLE CONTENT */}
                                {docProcConfigs.map((docProcCnf) => (
                                    <TableRow
                                        onClick={() => {
                                            setDocProcessingConfig(docProcCnf)
                                        }}
                                        sx={{
                                            cursor: 'pointer',
                                            backgroundColor: docProcessingConfig && docProcessingConfig.id === docProcCnf.id ? 'rgba(0, 0, 0, 0.1)' : 'inherit',
                                        }}
                                    >
                                        <TableCell>
                                            {parseDateTime(docProcCnf.datetime)}
                                        </TableCell>
                                        <TableCell>
                                            {docProcCnf.name}
                                        </TableCell>
                                        <TableCell>
                                            <MUILink
                                                component={Link}
                                                href={`/doc-proc-cnf/${docProcCnf.id}`}
                                                underline={'none'}
                                            >
                                                <OpenInNewIcon/>
                                            </MUILink>
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
                        onPageChange={(_, newPage) => {
                            setCurrPage(newPage + 1)
                        }}
                        rowsPerPage={TABLE_PAGE_LIMIT}
                        rowsPerPageOptions={[]}
                    />
                </Box>

                {/* DATA PEEK */}
                <Box
                    sx={{
                        width: '50%',
                        overflow: 'hidden',
                    }}
                    display="flex"
                    flexDirection="column"
                    gap={2}
                    maxHeight={416}
                >
                    {/* TOP PANEL */}
                    <Box
                        display={'flex'}
                        gap={1}
                    >
                        <Typography>
                            vec-col data-peek, docs: {vecColDocsCount}
                        </Typography>

                        <Tooltip title={'explore vec-col in detail'}>
                            <MUILink
                                component={Link}
                                href={`/vec-col/${name}/explore`}
                                underline={'none'}
                            >
                                <OpenInNewIcon/>
                            </MUILink>
                        </Tooltip>
                    </Box>

                    <Paper
                        sx={{
                            flex: 1,
                            overflow: 'hidden',
                            display: 'flex',
                            flexDirection: 'column',
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
                            {vecColPeek.map((peek, index) => (
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
                                            ID: <strong>{peek.id_}</strong>
                                        </Typography>

                                        <Typography >
                                            <strong>Embedding:</strong> {peek.embedding}
                                        </Typography>

                                        <Typography >
                                            <strong>Document:</strong> {peek.document}
                                        </Typography>

                                        <Typography >
                                            <strong>Metadata:</strong>
                                            <pre style={{ whiteSpace: 'pre-wrap', wordWrap: 'break-word' }}>
                                                {JSON.stringify(peek.metadata, null, 2)}
                                            </pre>
                                        </Typography>
                                    </CardContent>
                                </Card>
                            ))}
                        </Box>
                    </Paper>
                </Box>


            </Box>

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
                    onClose={() => setUrlDialog(false)}
                    scroll={scroll}
                    fullWidth={true}
                >
                    <DialogTitle>
                        add url
                    </DialogTitle>

                    <DialogContent
                        dividers={true}
                    >
                        <TextField
                            label={'url'}
                            variant={'standard'}
                            fullWidth={true}
                            value={selectedUrlInput}
                            onChange={(e) => setSelectedUrlInput(e.target.value)}
                            onKeyDown={(e) => {
                                if (e.key === 'Enter' && selectedUrlInput) {
                                    setSelectedUrls((prevUrls) => [...prevUrls, selectedUrlInput]);
                                    setSelectedUrlInput(null);
                                }
                            }}
                            placeholder={'enter url and press ENTER'}
                        />
                    </DialogContent>
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
            {(selectedFiles.length > 0 || selectedUrls.length > 0) && (
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