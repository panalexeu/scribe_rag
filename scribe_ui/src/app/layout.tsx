"use client";

import {useState} from "react";
import '@fontsource/roboto/500.css'; // default font for whole app
import {CssBaseline, Icon, Toolbar} from "@mui/material";
import Typography from "@mui/material/Typography";
import AppBar from "@mui/material/AppBar";
import {ThemeProvider} from "@mui/material";
import {IconButton} from "@mui/material";
import DarkModeIcon from '@mui/icons-material/DarkMode';
import LightModeIcon from '@mui/icons-material/LightMode';
import Drawer from '@mui/material/Drawer';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import Divider from '@mui/material/Divider';
import SettingsIcon from '@mui/icons-material/Settings';
import Box from '@mui/material/Box';
import KeyIcon from '@mui/icons-material/Key';

import {darkTheme, lightTheme} from "./theme";

export default function RootLayout(
    {children}: { children: React.ReactNode }
) {
    const [themeMode, setThemeMode] = useState(lightTheme);
    const listItemSize = 64;
    const drawerWidth = 256;

    return (
        <html lang="en">
        <head>
            <title>Scribe</title>
            <meta name="viewport" content="initial-scale=1, width=device-width"/>
        </head>

        <body>
        <ThemeProvider theme={themeMode}>
            <CssBaseline>
                {/*APP_BAR*/}
                <AppBar position={"static"} color={"transparent"}>
                    <Toolbar>
                        {/*<Typography variant={'h5'}>Scribe</Typography>*/}
                        <IconButton size={'large'} color={"inherit"} sx={{marginLeft: 'auto'}}
                                    onClick={() => themeMode === lightTheme ? setThemeMode(darkTheme) : setThemeMode(lightTheme)}
                        >
                            {themeMode === lightTheme ? <DarkModeIcon/> : <LightModeIcon/>}
                        </IconButton>
                    </Toolbar>
                </AppBar>

                {/*DRAWER*/}
                <Drawer
                    anchor={"left"}
                    variant={"permanent"}
                    sx={{
                        width: drawerWidth,
                        flexShrink: 0,
                        '& .MuiDrawer-paper': {
                            width: drawerWidth,
                            boxSizing: 'border-box',
                        }
                    }}
                >
                    {/*Logo*/}
                    <Toolbar>
                        <Typography variant={'h5'}>
                            Scribe
                        </Typography>
                    </Toolbar>
                    <Divider/>

                    {/*List*/}
                    <List disablePadding={true}>
                        <ListItem disablePadding={true} sx={{height:listItemSize}}>
                            <ListItemButton>
                                <ListItemIcon>
                                    <SettingsIcon/>
                                </ListItemIcon>
                                <ListItemText primary={"Settings"}/>
                            </ListItemButton>
                        </ListItem>
                        <Divider/>
                        <ListItem disablePadding={true} sx={{height:listItemSize}}>
                            <ListItemButton>
                                <ListItemIcon>
                                    <KeyIcon/>
                                </ListItemIcon>
                                <ListItemText primary={"Credentials"}/>
                            </ListItemButton>
                        </ListItem>
                        <Divider/>
                    </List>
                </Drawer>
            </CssBaseline>
        </ThemeProvider>
        </body>
        </html>
    );
}