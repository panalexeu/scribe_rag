import {z} from 'zod';

export const ApiKeyPostModel = z.object({
    name: z.string(),
    api_key: z.string()
});

export const ApiKeyPutModel = z.object({
    name: z.string().nullable()
});

export const ApiKeyResponseModel = z.object({
    id: z.number(),
    name: z.string(),
    api_key: z.string(),
    datetime: z.string()
})