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