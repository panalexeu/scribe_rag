import {Box, Breadcrumbs, Divider, IconButton, Tooltip, Typography} from "@mui/material";

export default function Page() {
    return (
        <Box
            display={'flex'}
            flexDirection={"column"}
            alignItems={'flex-start'}
            gap={2}
        >
            <Box display={'flex'} width={'100%'}>
                <Breadcrumbs>
                    <Typography variant={'h6'}>
                        scribe
                    </Typography>
                </Breadcrumbs>
            </Box>

            <Divider sx={{width: '100%'}}/>
        </Box>
    );
}