import List from "@mui/material/List";
import ListItem from "@mui/material/ListItem";
import ListItemButton from "@mui/material/ListItemButton";
import ListItemIcon from "@mui/material/ListItemIcon";
import SettingsIcon from "@mui/icons-material/Settings";
import ListItemText from "@mui/material/ListItemText";
import Divider from "@mui/material/Divider";
import KeyIcon from "@mui/icons-material/Key";
import TerminalIcon from '@mui/icons-material/Terminal';

import { useRouter } from 'next/navigation';

export default function NavList() {
    const router = useRouter();

    return (
        <List disablePadding={true}>

            {/* DASHBOARD */}
            <ListItem disablePadding={true}>
                <ListItemButton
                    onClick = {
                        () => router.push('/dashboard')
                    }
                >
                    <ListItemIcon>
                        <TerminalIcon/>
                    </ListItemIcon>
                    <ListItemText primary={"Dashboard"}/>
                </ListItemButton>
            </ListItem>
            <Divider/>

            {/* CREDERNTIALS */}
            <ListItem disablePadding={true}>
                <ListItemButton
                    onClick = {
                        () => router.push('/credentials')
                    }
                >
                    <ListItemIcon>
                        <KeyIcon/>
                    </ListItemIcon>
                    <ListItemText primary={"Credentials"}/>
                </ListItemButton>
            </ListItem>
            <Divider/>

            {/* SETTINGS */}
            <ListItem disablePadding={true}>
                <ListItemButton
                    onClick = {
                        () => router.push('/settings')
                    }
                >
                    <ListItemIcon>
                        <SettingsIcon/>
                    </ListItemIcon>
                    <ListItemText primary={"Settings"}/>
                </ListItemButton>
            </ListItem>
            <Divider/>
        </List>
    );
}