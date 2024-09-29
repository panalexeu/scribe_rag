import {
    Toolbar,
    Typography,
    IconButton,
    Tooltip
} from '@mui/material';
import EditIcon from '@mui/icons-material/Edit';
import LaunchIcon from '@mui/icons-material/Launch';
import DeleteIcon from '@mui/icons-material/Delete';


export default function ChatItem({name}: { name: string }) {
    return (
        <Toolbar>
            <Typography>{name}</Typography>

            {/* edit */}
            <Tooltip title={'Edit chat'}>
                <IconButton>
                    <EditIcon/>
                </IconButton>
            </Tooltip>

            {/* delete */}
            <Tooltip title={'Delete chat'}>
                <IconButton edge={'start'}>
                    <DeleteIcon/>
                </IconButton>
            </Tooltip>

            {/* launch */}
            <Tooltip title={'Open chat'}>
                <IconButton
                    sx={{
                        marginLeft: 'auto'
                    }}
                >
                    <LaunchIcon/>
                </IconButton>
            </Tooltip>
        </Toolbar>
    );
}