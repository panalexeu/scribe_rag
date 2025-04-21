import {z} from 'zod';

import {ChatModelResponseModel} from "@/src/app/chat-model/models";
import {SysPromptResponseModel} from '@/src/app/sys-prompt/models'
import {VectorCollectionResponseModel} from "@/src/app/vec-col/models";


export const BaseChatPostModel = z.object({
    name: z.string(),
    desc: z.string(),
    chat_model_id: z.number(),
    system_prompt_id: z.number().nullable(),
    vec_col_id: z.number().nullable()
})

export const BaseChatPutModel = z.object({
    name: z.string(),
    desc: z.string(),
    chat_model_id: z.number(),
    system_prompt_id: z.number().nullable(),
    vec_col_id: z.number().nullable()
})


export interface BaseChatResponseModel {
    id: number,
    name: string,
    desc: string,
    chat_model_id: number,
    chat_model: ChatModelResponseModel | null,
    system_prompt_id: number | null,
    system_prompt: SysPromptResponseModel | null,
    vec_col_id: number | null,
    vec_col: VectorCollectionResponseModel | null,
    datetime: string
}


export const BaseChatStreamModel = z.object({
    query_string: z.string(),
    doc_names: z.array(z.string()).nullable(),
    n_results: z.number().nullable()
})