import {Toolbar} from "@mui/material";
import Typography from "@mui/material/Typography";
import Divider from "@mui/material/Divider";
import Box from "@mui/material/Box";

export default function Logo() {
    return (
        <Box>
            <Toolbar>
                <Typography variant={'h5'}>
                    Scribe
                </Typography>
            </Toolbar>
            <Divider/>
        </Box>
    );
}