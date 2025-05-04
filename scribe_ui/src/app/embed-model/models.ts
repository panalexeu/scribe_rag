import {z} from 'zod';

import {ApiKeyResponseModel} from "@/src/app/api-key/models";

export const EmbeddingModelPostModel = z.object({
    name: z.string(),
    device: z.string(),
    api_key_credential_id: z.number()
})

export const EmbeddingModelPutModel = z.object({
    name: z.string().nullable(),
    device: z.string().nullable(),
    api_key_credential_id: z.number().nullable()
})

export interface EmbeddingModelResponseModel {
    id: number,
    name: string,
    device: string,
    api_key_credential_id: number,
    api_key_credential: ApiKeyResponseModel | null,
    datetime: string
}

export const EmbeddingModelName = Object.freeze({
    // local
    ALL_MINILM_L6_V2: 'all-MiniLM-L6-v2',
    XLM_ROBERTA_UA_DISTILLED: 'panalexeu/xlm-roberta-ua-distilled',

    // open ai
    TEXT_EMBEDDING_3_SMALL: 'text-embedding-3-small',

    // cohere
    EMBED_ENGLISH_LIGHT_V3_0: 'embed-english-light-v3.0',
    EMBED_MULTILINGUAL_LIGHT_V3_0: 'embed-multilingual-light-v3.0'
})

export const Device = Object.freeze({
    CPU: 'cpu',
    CUDA: 'cuda'
})