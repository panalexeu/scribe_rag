import {z} from 'zod';

export const SemDocProcCnfPostModel = z.object({
    name: z.string(),
    thresh: z.number(),
    max_chunk_size: z.number()
});

export const SemDocProcCnfPutModel = z.object({
    name: z.string(),
    thresh: z.number().nullable(),
    max_chunk_size: z.number().nullable()
});


export interface SemDocProcCnfResponseModel {
    id: number,
    name: string,
    thresh: number,
    max_chunk_size: number,
    datetime: string
}
