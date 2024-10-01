import {
    Box,
    Divider,
    Toolbar,
    Typography,
    Stack,
    Paper,
    TextField,
    InputAdornment,
    IconButton,
} from '@mui/material';
import SendIcon from '@mui/icons-material/Send';

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

            {/* Chat */}
            <Stack
                marginTop={1}
            >
                {/* LLM output*/}
                <Paper
                    variant={'outlined'}
                    sx={{
                        flexGrow: 1
                    }}
                >
                    <Typography>
                        LLM OUTPUT LLM OUTPUT LLM OUTPUT
                        LLM OUTPUT LLM OUTPUT LLM OUTPUT
                        LLM OUTPUT LLM OUTPUT LLM OUTPUT

                    </Typography>
                </Paper>

                {/* Input field*/}
                <Box
                    marginTop={1}
                    display={'flex'}
                    width={'100%'}
                >
                    <TextField
                        sx={{
                            flexGrow: 1
                        }}
                        multiline={true}
                        minRows={1}
                        maxRows={4}
                        placeholder={'Send an instruction...'}
                        slotProps={{
                            input: {
                                endAdornment: (
                                    <InputAdornment position={'end'}>
                                        <IconButton>
                                            <SendIcon/>
                                        </IconButton>
                                    </InputAdornment>
                                )
                            }
                        }}
                    >

                    </TextField>
                </Box>
            </Stack>
        </Box>
    );
}