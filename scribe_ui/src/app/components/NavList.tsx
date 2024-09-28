import List from "@mui/material/List";
import ListItem from "@mui/material/ListItem";
import ListItemButton from "@mui/material/ListItemButton";
import ListItemIcon from "@mui/material/ListItemIcon";
import SettingsIcon from "@mui/icons-material/Settings";
import ListItemText from "@mui/material/ListItemText";
import Divider from "@mui/material/Divider";
import KeyIcon from "@mui/icons-material/Key";

export default function NavList() {
    const listItemSize = 64;

    return (

        <List disablePadding={true}>
            <ListItem disablePadding={true} sx={{height: listItemSize}}>
                <ListItemButton>
                    <ListItemIcon>
                        <SettingsIcon/>
                    </ListItemIcon>
                    <ListItemText primary={"Settings"}/>
                </ListItemButton>
            </ListItem>
            <Divider/>
            <ListItem disablePadding={true} sx={{height: listItemSize}}>
                <ListItemButton>
                    <ListItemIcon>
                        <KeyIcon/>
                    </ListItemIcon>
                    <ListItemText primary={"Credentials"}/>
                </ListItemButton>
            </ListItem>
            <Divider/>
        </List>
    );
}