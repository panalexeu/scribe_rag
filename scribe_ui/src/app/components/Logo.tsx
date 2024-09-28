import {
    Toolbar,
    IconButton,
    Typography,
    Divider,
    Box
} from "@mui/material";
import HomeIcon from '@mui/icons-material/Home';

export default function Logo() {
    return (
        <Box>
            <Toolbar>
                <IconButton edge={'start'}>
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