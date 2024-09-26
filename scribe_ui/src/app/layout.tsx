import '@fontsource/roboto/500.css'; // default font for whole app
import {CssBaseline} from "@mui/material";

export default function RootLayout(
    {children}: { children: React.ReactNode }
) {
    return (
        <html lang="en">
        <head>
            <title>Scribe</title>
            <meta name="viewport" content="initial-scale=1, width=device-width"/>
        </head>

        <body>
        <CssBaseline>
            {children}
        </CssBaseline>
        </body>
        </html>
    );
}