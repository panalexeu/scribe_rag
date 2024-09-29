import {
    Box,
    TextField
} from '@mui/material';

export default function Page() {
    return (
        <Box>
            {/* First row*/}
            <Box>
                {/* Chat name */}
                <TextField
                    label={'Chat name'}
                />
            </Box>

        </Box>
    );
}