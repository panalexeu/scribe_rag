"use client";

import {useState} from "react";
import '@fontsource/roboto/500.css'; // default font for whole app
import {CssBaseline, Toolbar} from "@mui/material";
import AppBar from "@mui/material/AppBar";
import {ThemeProvider} from "@mui/material";
import {IconButton} from "@mui/material";
import DarkModeIcon from '@mui/icons-material/DarkMode';
import LightModeIcon from '@mui/icons-material/LightMode';
import Drawer from '@mui/material/Drawer';
import Box from '@mui/material/Box';

import {darkTheme, lightTheme} from "./theme";
import NavList from './components/NavList';
import Logo from './components/Logo';

export default function RootLayout(
    {children}: { children: React.ReactNode }
) {
    const [themeMode, setThemeMode] = useState(lightTheme);
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
                <AppBar
                    position={"static"}
                    color={"transparent"}
                    sx={{
                        width: `calc(100% - ${drawerWidth}px)`,
                        ml: `${drawerWidth}px`
                    }}
                >
                    <Toolbar>
                        <IconButton  sx={{marginLeft: 'auto'}}
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
                        '& .MuiDrawer-paper': {
                            width: drawerWidth,
                            boxSizing: 'border-box',
                        }
                    }}
                    color={"transparent"}
                >
                    <Logo/>
                    <NavList/>
                </Drawer>

                {/* Main page content */}
                <Box
                    marginLeft={`${drawerWidth}px`}
                    padding={1}
                >
                    {children}
                </Box>
            </CssBaseline>
        </ThemeProvider>
        </body>
        </html>
    );
}