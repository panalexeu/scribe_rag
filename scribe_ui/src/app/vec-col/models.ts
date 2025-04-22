import {z} from 'zod';
import {EmbeddingModelResponseModel} from '@/src/app/embed-model/models';

export const VectorCollectionPostModel = z.object({
    name: z.string(),
    embedding_model_id: z.number(),
    distance_func: z.string()
})

export interface VectorCollectionResponseModel {
    id: number,
    name: string,
    embedding_model: EmbeddingModelResponseModel | null,
    distance_func: string,
    datetime: string
}

export const DistanceFunction = Object.freeze({
    L2: 'l2',
    IP: 'ip',
    COSINE: 'cosine'
})

export interface MetadataModel {
    filename: string,
    filetype: string,
    languages: [string],
    page_number: number
}

export interface VectorDocumentResponseModel {
    id_: string,
    distance: number | null,
    embedding: string,
    document: string,
    metadata: MetadataModel
}