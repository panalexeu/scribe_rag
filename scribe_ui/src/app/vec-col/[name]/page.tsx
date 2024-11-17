'use client';

import {
    Breadcrumbs,
    Divider,
    Link as MUILink,
    Snackbar,
    Typography,
    Box
} from "@mui/material";
import {useRouter, useParams} from "next/navigation";
import {useState, useEffect} from "react";

import {VectorCollectionResponseModel} from '../models';
import {API_URL, TABLE_PAGE_LIMIT} from "@/src/constants";
import Link from "next/link";

export default function Page() {
    const {name} = useParams();
    const router = useRouter();
    const [openSnackbar, setOpenSnackbar] = useState(false);
    const [snackbarMessage, setSnackbarMessage] = useState('');

    const [vectorCollection, setVectorCollection] = useState<VectorCollectionResponseModel>(null)
    const [distanceFunction, setDistanceFunction] = useState(null);

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