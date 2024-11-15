import { format, parseISO } from 'date-fns';

export function parseDateTime(datetime: string): string {
    return format(parseISO(datetime), 'MM-dd-yyyy, HH:mm');
}