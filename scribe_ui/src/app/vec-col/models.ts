import {z} from 'zod';
import {EmbeddingModelResponseModel} from '@/src/app/embed-model/models';

export const VectorCollectionPostModel = z.object({
    name: z.string(),
    embedding_model_id: z.number(),
    distance_func: z.string().nullable()
})

export interface VectorCollectionResponseModel {
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

export interface VectorDocumentResponseModel {
    id_: string,
    distance: number | null,
    embedding: string,
    document: string,
    metadata: Object
}