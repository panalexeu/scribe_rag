'use client';

import {
    List,
    ListItem,
    ListItemButton,
    ListItemIcon,
    ListItemText,
    Divider,
} from '@mui/material';
import PendingActionsIcon from '@mui/icons-material/PendingActions';
import DescriptionIcon from '@mui/icons-material/Description';
import KeyIcon from "@mui/icons-material/Key";
import DataArrayIcon from '@mui/icons-material/DataArray';
import {useRouter} from 'next/navigation';
import SmartToyIcon from '@mui/icons-material/SmartToy';
import PolylineIcon from '@mui/icons-material/Polyline';
import FunctionsIcon from '@mui/icons-material/Functions';
import ChatBubbleIcon from '@mui/icons-material/ChatBubble';

export default function NavList() {
    const router = useRouter();

    return (
        <List disablePadding={true}>
            {/* api-key */}
            <ListItem disablePadding={true}>
                <ListItemButton
                    onClick={
                        () => router.push('/api-key')
                    }
                >
                    <ListItemIcon>
                        <KeyIcon/>
                    </ListItemIcon>
                    <ListItemText primary={"api-key"}/>
                </ListItemButton>
            </ListItem>
            <Divider/>

            {/* sys-prompt */}
            <ListItem disablePadding={true}>
                <ListItemButton
                    onClick={
                        () => router.push('/sys-prompt')
                    }
                >
                    <ListItemIcon>
                        <DescriptionIcon/>
                    </ListItemIcon>
                    <ListItemText primary={"sys-prompt"}/>
                </ListItemButton>
            </ListItem>
            <Divider/>

            {/* doc-proc-cnf */}
            <ListItem disablePadding={true}>
                <ListItemButton
                    onClick={
                        () => router.push('/doc-proc-cnf')
                    }
                >
                    <ListItemIcon>
                        <PendingActionsIcon/>
                    </ListItemIcon>
                    <ListItemText primary={"doc-proc-cnf"}/>
                </ListItemButton>
            </ListItem>
            <Divider/>

            {/* sem-doc-proc-cnf */}
            <ListItem disablePadding={true}>
                <ListItemButton
                    onClick={
                        () => router.push('/sem-doc-proc-cnf')
                    }
                >
                    <ListItemIcon>
                        <FunctionsIcon/>
                    </ListItemIcon>
                    <ListItemText primary={"sem-doc-proc-cnf"}/>
                </ListItemButton>
            </ListItem>
            <Divider/>

            {/* embed-model */}
            <ListItem disablePadding={true}>
                <ListItemButton
                    onClick={
                        () => router.push('/embed-model')
                    }
                >
                    <ListItemIcon>
                        <DataArrayIcon/>
                    </ListItemIcon>
                    <ListItemText primary={"embed-model"}/>
                </ListItemButton>
            </ListItem>
            <Divider/>

            {/* chat-model */}
            <ListItem disablePadding={true}>
                <ListItemButton
                    onClick={
                        () => router.push('/chat-model')
                    }
                >
                    <ListItemIcon>
                        <SmartToyIcon/>
                    </ListItemIcon>
                    <ListItemText primary={"chat-model"}/>
                </ListItemButton>
            </ListItem>
            <Divider/>

            {/* vec-col */}
            <ListItem disablePadding={true}>
                <ListItemButton
                    onClick={
                        () => router.push('/vec-col')
                    }
                >
                    <ListItemIcon>
                        <PolylineIcon/>
                    </ListItemIcon>
                    <ListItemText primary={"vec-col"}/>
                </ListItemButton>
            </ListItem>
            <Divider/>

            {/* base-chat */}
            <ListItem disablePadding={true}>
                <ListItemButton
                    onClick={
                        () => router.push('/base-chat')
                    }
                >
                    <ListItemIcon>
                        <ChatBubbleIcon/>
                    </ListItemIcon>
                    <ListItemText primary={"base-chat"}/>
                </ListItemButton>
            </ListItem>
            <Divider/>

        </List>
    );
}