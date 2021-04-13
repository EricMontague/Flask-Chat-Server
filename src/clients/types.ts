export interface ServerError {
    message: string;
    status_code?: number;
    url?: string
};

export interface FetchOptions {
    headers?: {[x: string]: string};
    method?: string;
    url?: string;
    credentials?: 'omit' | 'same-origin' | 'include';
    body?: any;
};

export interface ClientResponse<T> {
    response: Response;
    headers: Headers;
    data: T;
};