// importing mui by default fonts roboto
import '@fontsource/roboto/300.css';
import '@fontsource/roboto/400.css';
import '@fontsource/roboto/500.css';
import '@fontsource/roboto/700.css';


export default function RootLayout(
    {children}: { children: React.ReactNode }
) {
    return (
        <html lang="en">
            <head>
                <title>Scribe</title>
            </head>

            <body>
                {children}
            </body>
        </html>
    );
}