import {
    Box, Divider,
    Toolbar, Typography
} from '@mui/material';

export default function Page({params}: {params: {chat_id: string}}) {
    return(
        <Box>
            {/* Info */}
            <Toolbar>
                <Typography
                    variant={'h6'}
                >
                    {params.chat_id}
                </Typography>
            </Toolbar>
            <Divider/>
        </Box>
    );
}