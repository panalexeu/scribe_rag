'use client';

import {
    Toolbar,
    IconButton,
    Typography,
    Divider,
    Box,
    Tooltip
} from "@mui/material";
import {useRouter} from "next/navigation";
import HomeIcon from '@mui/icons-material/Home';

export default function Logo() {
    const router = useRouter();
    return (
        <Box>
            <Toolbar>
                <Tooltip title={'Home'}>
                    <IconButton
                        edge={'start'}
                        onClick={
                            () => router.push('/')
                        }
                    >
                        <HomeIcon/>
                    </IconButton>
                </Tooltip>
                
                <Typography variant={'h5'}>
                    Scribe
                </Typography>
            </Toolbar>
            <Divider/>
        </Box>
    );
}