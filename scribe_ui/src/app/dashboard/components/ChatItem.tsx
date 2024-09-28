import {
    Toolbar,
    Typography,
    IconButton
} from '@mui/material';
import EditIcon from '@mui/icons-material/Edit';
import LaunchIcon from '@mui/icons-material/Launch';


export default function ChatItem({name}: { name: string }) {
    return (
        <Toolbar>
            <Typography>{name}</Typography>

            {/* edit */}
            <IconButton>
                <EditIcon/>
            </IconButton>

            {/* launch */}
            <IconButton
                sx={{
                    marginLeft: 'auto'
                }}
            >
                <LaunchIcon/>
            </IconButton>
        </Toolbar>
    );
}