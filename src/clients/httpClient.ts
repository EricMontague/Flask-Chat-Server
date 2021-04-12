import { authClient } from './authClient';
import { RegistrationInfo, Tokens, User } from '../features/users/usersSlice';
import { ServerError, FetchOptions, ClientResponse } from './types';

export class ClientError extends Error implements ServerError {
    url?: string;
    server_error_id?: string;
    status_code?: number;
    message: string;

    constructor(baseUrl: string, data: ServerError) {
        super(data.message + ':' + baseUrl);

        this.message = data.message;
        this.url = data.url;
        this.server_error_id = data.server_error_id;
        this.status_code = data.status_code;
        
        // Ensure message is treated as a property of this class when object spreading. Without this,
        // copying the object by using `{...error}` would not include the message.
        Object.defineProperty(this, 'message', { enumerable: true });
    }

};

class HTTPClient {

    baseUrl: string;
    apiVersion: string;
    logToConsole: boolean;
    tokens: Tokens;

    constructor(baseUrl: string, apiVersion: string) {
        this.baseUrl = baseUrl;
        this.apiVersion = apiVersion;
        this.logToConsole = process.env.REACT_APP_LOG_TO_CONSOLE === 'true';
        this.tokens = {access: '', refresh: ''};

    }

    doFetch = async <T>(url: string, options: FetchOptions): Promise<T> => {
        const {data} = await this.doFetchWithResponse<T>(url, options);
        return data;
    };

    doFetchWithResponse = async <T>(url: string, options: FetchOptions): Promise<ClientResponse<T>> => {
        const response = await fetch(url, this.addHeaders(options));

        let data;
        try {
            data = await response.json();
        } catch(err) {
            throw new ClientError(this.getBaseUrl(), {
                message: 'Received invalid response from the server',
                url
            })
        }

        // Fetch won't catch 4xx or 5xx errors, but will instead set the ok property to false
        if (response.ok) {
            return {
                data,
                response,
                headers: response.headers,
            }
        }

        const message = data.message || '';

        if (this.logToConsole) {
            console.error(message); // eslint-disable-line no-console
        }

        throw new ClientError(this.getBaseUrl(), {
            message,
            url,
            server_error_id: data.error_id,
            status_code: data.status_code
        })
    };

    getBaseUrl() {
        return this.baseUrl;
    }

    getAPIVersion() {
        return this.apiVersion;
    }

    getBaseRoute() {
        return `${this.getBaseUrl()}/${this.getAPIVersion()}`;
    }

    getAuthRoute() {
        return `${this.getBaseRoute()}/auth`;
    }

    getUserRoute() {
        return `${this.getBaseRoute()}/users`;
    }

    addHeaders(options: FetchOptions) {
        const newOptions = {...options};
        const headers: {[x: string]: string} = {};
        // headers['Authorization'] = `Bearer ${this.token}`;
        headers['Content-Type'] = 'application/json';
        headers['Accept'] = 'application/json';
        newOptions['headers'] = headers
        return newOptions;
    }

    getTokens() {
        return this.tokens;
    }

    setTokens(tokens: Tokens) {
        this.tokens = tokens;
    }

    async login(email: string, password: string) {
        const options = {
            method: 'POST',
            body: JSON.stringify({email, password})
        };
        return await this.doFetch<Tokens>(`${this.getAuthRoute()}/login`, options);
    }

    async register(registrationInfo: RegistrationInfo) {
        const options = {
            method: 'POST',
            body: JSON.stringify(registrationInfo)
        };
        return await this.doFetch<User>(`${this.getAuthRoute()}/register`, options);
    }

    async logout() {
        const options = {method: 'DELETE'};
        const { response } = await this.doFetchWithResponse<any>(`${this.getAuthRoute()}/revoke_tokens`, options);
        return response;
    }

    async getUserById(userId: string) {
        return await this.doFetch<User>(`${this.getUserRoute()}/${userId}`, {})
    }

    async getUserByUsername(username: string) {
        return await this.doFetch<User>(`${this.getUserRoute()}/username/${username}`, {});
    }
}

export const httpClient = new HTTPClient(process.env.REACT_APP_API_BASE_URL!, process.env.REACT_APP_API_VERSION!);
