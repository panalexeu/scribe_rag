'use client';

import {
    List,
    ListItem,
    ListItemButton,
    ListItemIcon,
    ListItemText,
    Divider
} from '@mui/material';
import KeyIcon from "@mui/icons-material/Key";
import { useRouter } from 'next/navigation';

export default function NavList() {
    const router = useRouter();

    return (
        <List disablePadding={true}>
            {/* CREDERNTIALS */}
            <ListItem disablePadding={true}>
                <ListItemButton
                    onClick = {
                        () => router.push('/api-key')
                    }
                >
                    <ListItemIcon>
                        <KeyIcon/>
                    </ListItemIcon>
                    <ListItemText primary={"Api Key Credential"}/>
                </ListItemButton>
            </ListItem>
            <Divider/>
        </List>
    );
}