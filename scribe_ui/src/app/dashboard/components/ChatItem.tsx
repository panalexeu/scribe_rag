import {
    Toolbar,
    Typography,
    IconButton,
    Tooltip
} from '@mui/material';
import EditIcon from '@mui/icons-material/Edit';
import LaunchIcon from '@mui/icons-material/Launch';
import DeleteIcon from '@mui/icons-material/Delete';
import { useRouter } from 'next/navigation';


export default function ChatItem({name}: { name: string }) {
    const router = useRouter();

    return (
        <Toolbar>
            <Typography>{name}</Typography>

            {/* edit */}
            <Tooltip
                title={'Edit chat'}
            >
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
                    edge={'end'}
                    sx={{
                        marginLeft: 'auto'
                    }}
                    onClick={
                        () => router.push(`/dashboard/instruction-chat/${name}`)
                    }
                >
                    <LaunchIcon/>
                </IconButton>
            </Tooltip>
        </Toolbar>
    );
}