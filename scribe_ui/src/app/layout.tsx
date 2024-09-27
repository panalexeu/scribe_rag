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

import {darkTheme, lightTheme} from "./theme";
import {light} from "@mui/material/styles/createPalette";

export default function RootLayout(
    {children}: { children: React.ReactNode }
) {
    const [themeMode, setThemeMode] = useState(lightTheme);

    return (
        <html lang="en">
        <head>
            <title>Scribe</title>
            <meta name="viewport" content="initial-scale=1, width=device-width"/>
        </head>

        <body>
        <ThemeProvider theme={themeMode}>
            <CssBaseline>
                <AppBar position={"static"} color={"transparent"}>
                    <Toolbar>
                        <Typography variant={'h5'}>Scribe</Typography>
                        <IconButton size={'large'} color={"inherit"}
                                    onClick={() => themeMode === lightTheme ? setThemeMode(darkTheme) : setThemeMode(lightTheme)}
                        >
                            {themeMode === lightTheme? <DarkModeIcon/>: <LightModeIcon/>}
                        </IconButton>
                    </Toolbar>
                </AppBar>
                {children}
            </CssBaseline>
        </ThemeProvider>
        </body>
        </html>
    );
}