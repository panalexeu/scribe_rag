import {
    CircularProgress,
    Box
} from "@mui/material";


export default function Loading() {
    return (
        <Box
            display={'flex'}
            alignItems={'center'}
            justifyContent={'center'}
            width={'100%'}
            height={'100%'}
        >
            <CircularProgress
                size={64}
            />
        </Box>
    );
}