import {
    Toolbar,
    IconButton,
    Typography,
    Divider,
    Box
} from "@mui/material";
import HomeIcon from '@mui/icons-material/Home';
import { useRouter } from 'next/navigation';

export default function Logo() {
    const router = useRouter();

    return (
        <Box>
            <Toolbar>
                <IconButton
                    edge={'start'}
                    onClick={
                        () => router.push('/')
                    }
                >
                    <HomeIcon/>
                </IconButton>
                <Typography variant={'h5'}>
                    Scribe
                </Typography>
            </Toolbar>
            <Divider/>
        </Box>
    );
}