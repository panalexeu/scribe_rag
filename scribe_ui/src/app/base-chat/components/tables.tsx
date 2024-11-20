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
    Typography,
} from '@mui/material';
import {parseDateTime} from "@/src/utils";
import {TABLE_PAGE_LIMIT} from "@/src/constants";

// SysPromptTable
export function SysPromptTable(
    {
        sysPrompts,
        count,
        currPage,
        setCurrPage,
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
                                    backgroundColor: sysPrompt.id === setSelectedItem.id ? 'rgba(0, 0, 0, 0.1)' : 'inherit',
                                }}
                            >
                                <TableCell>{parseDateTime(sysPrompt.datetime)}</TableCell>
                                <TableCell>{sysPrompt.name}</TableCell>
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
                                    backgroundColor: chatModel.id === setSelectedItem.id ? 'rgba(0, 0, 0, 0.1)' : 'inherit',
                                }}
                            >
                                <TableCell>{parseDateTime(chatModel.datetime)}</TableCell>
                                <TableCell>{chatModel.name}</TableCell>
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

export function VecColTable(
    {
        vectorCollections,
        count,
        currPage,
        setCurrPage,
        setSelectedItem,
    }) {
    return (
        <Box display={'flex'} flexDirection={'column'}>
            <TableContainer>
                <Table>
                    <TableHead>
                        <TableRow>
                            <TableCell>name</TableCell>
                            <TableCell>embedding</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {vectorCollections.map((vecCol, index) => (
                            <TableRow
                                key={index}
                                onClick={() => setSelectedItem(vecCol)}
                                sx={{
                                    cursor: 'pointer',
                                    backgroundColor: vecCol.name === setSelectedItem.name ? 'rgba(0, 0, 0, 0.1)' : 'inherit',
                                }}
                            >
                                <TableCell>{vecCol.name}</TableCell>
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
