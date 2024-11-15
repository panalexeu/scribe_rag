import {z} from 'zod';

export const ApiKeyPostModel = z.object({
    name: z.string(),
    api_key: z.string()
});

export const ApiKeyPutModel = z.object({
    name: z.string().nullable()
});

export interface ApiKeyResponseModel {
    id: number,
    name: string,
    api_key: string,
    datetime: string
}
