'use client';

import {Breadcrumbs, Divider, Link as MUILink, Typography, Box} from "@mui/material";
import Link from "next/link";
import {useParams, useRouter} from "next/navigation";

export default function Page() {
    const {id} = useParams();

    return (
        <Box
            display={'flex'}
            flexDirection={"column"}
            alignItems={'flex-start'}
            gap={2}
        >
            {/*TOP PANEL*/}
            <Breadcrumbs>
                <Typography variant={'h6'}>
                    <MUILink
                        component={Link}
                        href={'/base-chat'}
                        underline={'none'}
                    >
                        base-chat
                    </MUILink>
                </Typography>
                <Typography variant={'h6'}>
                    <MUILink
                        component={Link}
                        href={`/base-chat/${id}`}
                        underline={'none'}
                    >
                        {id}
                    </MUILink>
                </Typography>
                <Typography variant={'h6'}>
                    stream
                </Typography>
            </Breadcrumbs>

            <Divider sx={{width: '100%'}}/>

        </Box>
    );
}