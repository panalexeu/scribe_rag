import {Toolbar} from "@mui/material";
import {Divider} from "@mui/material";
import {Box} from "@mui/material";
import Typography from "@mui/material/Typography";
import IconButton from '@mui/material/IconButton';
import AddIcon from '@mui/icons-material/Add';

export default function Page() {
    return (
        <Box padding={1}>
            <Toolbar>
                <Typography variant={'h6'}>Chats</Typography>
                <IconButton
                    sx={{marginLeft: 'auto'}}
                >
                    <AddIcon/>
                </IconButton>
            </Toolbar>
            <Divider/>
        </Box>
    );
}