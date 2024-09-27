import AppBar from '@mui/material/AppBar';
import Typography from '@mui/material/Typography';
import {Toolbar} from "@mui/material";

export default function Page() {
    return (
        <AppBar position={"static"} color={"transparent"}>
            <Toolbar>
                <Typography variant={'h5'}>Scribe</Typography>
            </Toolbar>
        </AppBar>
    );
}