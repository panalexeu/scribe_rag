import {z} from 'zod';

export const DocProcCnfPostModel = z.object({
    name: z.string(),
    postprocessors: z.array(z.string()).nullable(),
    chunking_strategy: z.string().nullable(),
    max_characters: z.number().nullable(),
    new_after_n_chars: z.number().nullable(),
    overlap: z.number().nullable(),
    overlap_all: z.boolean().nullable()
});

export const DocProcCnfPutModel = z.object({
    name: z.string().nullable(),
    postprocessors: z.string().nullable(),
    chunking_strategy: z.string().nullable(),
    max_characters: z.number().nullable(),
    new_after_n_chars: z.number().nullable(),
    overlap: z.number().nullable(),
    overlap_all: z.boolean().nullable()
});


export interface DocProcCnfResponseModel {
    id: number,
    name: string,
    postprocessors: string | null,
    chunking_strategy: string | null,
    max_characters: number | null,
    new_after_n_chars: number | null,
    overlap: number | null,
    overlap_all: boolean | null,
    datetime: string
}

export const Postprocessor = Object.freeze({
    BYTES_STRING_TO_STRING: "bytes_string_to_string",
    CLEAN: "clean",
    CLEAN_BULLETS: "clean_bullets",
    CLEAN_DASHES: "clean_dashes",
    CLEAN_NON_ASCII_CHARS: "clean_non_ascii_chars",
    CLEAN_ORDERED_BULLETS: "clean_ordered_bullets",
    CLEAN_TRAILING_PUNCTUATION: "clean_trailing_punctuation",
    GROUP_BROKEN_PARAGRAPHS: "group_broken_paragraphs",
    REMOVE_PUNCTUATION: "remove_punctuation",
    REPLACE_UNICODE_QUOTES: "replace_unicode_quotes"

})

export const ChunkingStrategy = Object.freeze({
    BASIC: "basic",
    BY_TITLE: "by_title"
})
