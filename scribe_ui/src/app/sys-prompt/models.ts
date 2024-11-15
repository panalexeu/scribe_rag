import {z} from 'zod';

export const SysPromptPostModel = z.object({
    name: z.string(),
    content: z.string()
});

export const SysPromptPutModel = z.object({
    name: z.string().nullable(),
    content: z.string().nullable()
})

export interface SysPromptResponseModel {
    id: number,
    name: string,
    content: string,
    datetime: string
}