import {z} from 'zod';

import {ApiKeyResponseModel} from "@/src/app/api-key/models";

export const ChatModelPostModel = z.object({
    name: z.string(),
    api_key_credential_id: z.number(),
    temperature: z.number().nullable(),
    top_p: z.number().nullable(),
    base_url: z.string().nullable(),
    max_tokens: z.number().nullable(),
    max_retries: z.number().nullable(),
    stop_sequences: z.array(z.string()).nullable()
});

export const ChatModelPutModel = z.object({
    name: z.string().nullable(),
    api_key_credential_id: z.number().nullable(),
    temperature: z.number().nullable(),
    top_p: z.number().nullable(),
    base_url: z.string().nullable(),
    max_tokens: z.number().nullable(),
    max_retries: z.number().nullable(),
    stop_sequences: z.string().nullable()
});

export interface ChatModelResponseModel {
    id: number,
    name: string,
    api_key_credential_id: number,
    api_key_credential: ApiKeyResponseModel | null,
    temperature: number | null,
    top_p: number | null,
    base_url: string | null,
    max_tokens: number | null,
    max_retries: number | null,
    stop_sequences: string | null,
    datetime: string
}

export const ChatModelName = Object.freeze({
    // open ai
    GPT_4O_MINI: "gpt-4o-mini",
    GPT_4O: "gpt-4o",

    // cohere
    COMMAND_R_PLUS: "command-r-plus",
    COMMAND: "command",

    // anthropic
    CLAUDE_3_5_SONNET_20241022: "claude-3-5-sonnet-20241022",
    CLAUDE_3_5_HAIKU_20241022: "claude-3-5-haiku-20241022",
    CLAUDE_3_OPUS_20240229: "claude-3-opus-20240229",
    CLAUDE_3_SONNET_20240229: "claude-3-sonnet-20240229",
    CLAUDE_3_HAIKU_20240307: "claude-3-haiku-20240307"
})