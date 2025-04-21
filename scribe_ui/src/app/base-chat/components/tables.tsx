import React from 'react';
import {
    Box,
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableHead,
    TablePagination,
    TableRow,
    Link as MUILink,
} from '@mui/material';
import {parseDateTime} from "@/src/utils";
import {TABLE_PAGE_LIMIT} from "@/src/constants";
import Link from "next/link";

// SysPromptTable
export function SysPromptTable(
    {
        sysPrompts,
        count,
        currPage,
        setCurrPage,
        selectedItem,
        setSelectedItem,
    }) {
    return (
        <Box display={'flex'} flexDirection={'column'}>
            <TableContainer>
                <Table>
                    <TableHead>
                        <TableRow>
                            <TableCell>date</TableCell>
                            <TableCell>name</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {sysPrompts.map((sysPrompt) => (
                            <TableRow
                                key={sysPrompt.id}
                                onClick={() => setSelectedItem(sysPrompt)}
                                sx={{
                                    cursor: 'pointer',
                                    backgroundColor: sysPrompt.id === selectedItem?.id ? 'rgba(0, 0, 0, 0.1)' : 'inherit',
                                }}
                            >
                                <TableCell>{parseDateTime(sysPrompt.datetime)}</TableCell>
                                <TableCell>
                                    <MUILink
                                        component={Link}
                                        href={`/sys-prompt/${sysPrompt.id}`}
                                    >
                                        {sysPrompt.name}
                                    </MUILink>
                                </TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </TableContainer>
            <TablePagination
                page={currPage - 1}
                count={count}
                onPageChange={(_, newPage) => setCurrPage(newPage + 1)}
                rowsPerPage={TABLE_PAGE_LIMIT}
                rowsPerPageOptions={[]}
            />
        </Box>
    );
}

// ChatModelTable
export function ChatModelTable(
    {
        chatModels,
        count,
        currPage,
        setCurrPage,
        selectedItem,
        setSelectedItem,
    }) {
    return (
        <Box display={'flex'} flexDirection={'column'}>
            <TableContainer>
                <Table>
                    <TableHead>
                        <TableRow>
                            <TableCell>date</TableCell>
                            <TableCell>name</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {chatModels.map((chatModel) => (
                            <TableRow
                                key={chatModel.id}
                                onClick={() => setSelectedItem(chatModel)}
                                sx={{
                                    cursor: 'pointer',
                                    backgroundColor: chatModel.id === selectedItem?.id ? 'rgba(0, 0, 0, 0.1)' : 'inherit',
                                }}
                            >
                                <TableCell>{parseDateTime(chatModel.datetime)}</TableCell>
                                <TableCell>
                                    <MUILink
                                        component={Link}
                                        href={`/chat-model/${chatModel.id}`}
                                    >
                                        {chatModel.name}
                                    </MUILink>
                                </TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </TableContainer>
            <TablePagination
                page={currPage - 1}
                count={count}
                onPageChange={(_, newPage) => setCurrPage(newPage + 1)}
                rowsPerPage={TABLE_PAGE_LIMIT}
                rowsPerPageOptions={[]}
            />
        </Box>
    );
}

// VecColTable
export function VecColTable(
    {
        vectorCollections,
        count,
        currPage,
        setCurrPage,
        selectedItem,
        setSelectedItem,
    }) {
    return (
        <Box display={'flex'} flexDirection={'column'}>
            <TableContainer>
                <Table>
                    <TableHead>
                        <TableRow>
                            <TableCell>date</TableCell>
                            <TableCell>name</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {vectorCollections.map((vecCol, index) => (
                            <TableRow
                                key={index}
                                onClick={() => setSelectedItem(vecCol)}
                                sx={{
                                    cursor: 'pointer',
                                    backgroundColor: vecCol.name === selectedItem?.name ? 'rgba(0, 0, 0, 0.1)' : 'inherit',
                                }}
                            >
                                <TableCell>
                                    {parseDateTime(vecCol.datetime)}
                                </TableCell>
                                <TableCell>
                                    <MUILink
                                        component={Link}
                                        href={`/vec-col/${vecCol.id}`}
                                    >
                                        {vecCol.name}
                                    </MUILink>
                                </TableCell>
                                <TableCell>{vecCol.embedding_function}</TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </TableContainer>
            <TablePagination
                page={currPage - 1}
                count={count}
                onPageChange={(_, newPage) => setCurrPage(newPage + 1)}
                rowsPerPage={TABLE_PAGE_LIMIT}
                rowsPerPageOptions={[]}
            />
        </Box>
    );
}
