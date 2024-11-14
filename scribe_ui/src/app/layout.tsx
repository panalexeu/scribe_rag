import '@fontsource/roboto/500.css'; // default font for whole app
import {
    CssBaseline,
    AppBar,
    Drawer,
    Box,
    Toolbar
} from '@mui/material';
import NavList from './components/NavList';
import Logo from './components/Logo';

export default function RootLayout(
    {children}: { children: React.ReactNode }
) {
    const drawerWidth = 256;

    return (
        <html lang="en">
        <head>
            <title>Scribe</title>
            <meta name="viewport" content="initial-scale=1, width=device-width"/>
        </head>

        <body>
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

                <Toolbar/>

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
        </body>
        </html>
    );
}