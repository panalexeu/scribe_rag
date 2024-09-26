import AppBar from '@mui/material/AppBar';
import Typography from '@mui/material/Typography';
import {Box} from "@mui/material";
import {IconButton} from "@mui/material";
import MenuIcon from '@mui/icons-material/Menu';
import {Toolbar} from "@mui/material";

export default function Page() {
    return (

        <AppBar position={"static"}>
            <Toolbar>
                <IconButton
                    size={"large"}
                    color={"inherit"}
                    edge={"start"}
                >
                    <MenuIcon/>
                </IconButton>
            </Toolbar>
        </AppBar>
    );
}