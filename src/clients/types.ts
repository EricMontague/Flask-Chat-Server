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
    mode?: 'same-origin' | 'no-cors' | 'cors' | 'navigate';
};

export interface ClientResponse<T> {
    response: Response;
    headers: Headers;
    data: T;
};

export interface AuthCredentials {
    type: 'http_basic_auth' | 'jwt';
    credentials: string;
};

export interface AuthInfo {
    access: string;
    refresh: string;
    username: string;
};