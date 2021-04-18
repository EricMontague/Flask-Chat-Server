import { RegistrationInfo, Tokens, User } from '../features/users/usersSlice';
import { ServerError, FetchOptions, ClientResponse, AuthCredentials } from './types';
import { JWT, HTTP_BASIC_AUTH } from '../constants';

export class ClientError extends Error implements ServerError {
    url?: string;
    status_code?: number;
    message: string;

    constructor(baseUrl: string, data: ServerError) {
        super(data.message + ':' + baseUrl);

        this.message = data.message;
        this.url = data.url;
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

    doFetch = async <T>(url: string, options: FetchOptions, authCredentials?: AuthCredentials): Promise<T> => {
        const {data} = await this.doFetchWithResponse<T>(url, options, authCredentials);
        return data;
    };
    
    doFetchWithResponse = async <T>(url: string, options: FetchOptions, authCredentials?: AuthCredentials): Promise<ClientResponse<T>> => {
        const newOptions: FetchOptions = this.addExtraOptions(options, authCredentials);
        const response = await fetch(url, newOptions);

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

        const message = data.error || data.errors || '';

        if (this.logToConsole) {
            console.error(message); // eslint-disable-line no-console
        }

        throw new ClientError(this.getBaseUrl(), {
            message,
            url,
            status_code: response.status
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

    addExtraOptions(options: FetchOptions, authCredentials?: AuthCredentials) {
        const newOptions = {...options};
        const headers: {[x: string]: string} = {};
        if (authCredentials && authCredentials.type === JWT) {
            headers['Authorization'] = `Bearer ${authCredentials.credentials}`;
        } else if (authCredentials && authCredentials.type === HTTP_BASIC_AUTH) {
            headers['Authorization'] = `Basic ${authCredentials.credentials}`;
        }
        
        headers['Content-Type'] = 'application/json';
        headers['Accept'] = 'application/json';
        newOptions['headers'] = headers;
        return newOptions;
    }

    getTokens() {
        return this.tokens;
    }

    setTokens(tokens: Tokens) {
        this.tokens = tokens;
    }

    async login(username: string, password: string) {
        const options = {
            method: 'POST',
            body: JSON.stringify({username, password})
        };
        const authCredentials: AuthCredentials = {
            type: HTTP_BASIC_AUTH, credentials: btoa(username + ':' + password)
        };
        const tokens = await this.doFetch<Tokens>(`${this.getAuthRoute()}/login`, options, authCredentials);
        this.setTokens(tokens);
        return tokens;
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
        const authCredentials: AuthCredentials = {type: JWT, credentials: this.getTokens().access};
        const { response } = await this.doFetchWithResponse<any>(`${this.getAuthRoute()}/revoke_tokens`, options, authCredentials);
        return response;
    }

    async getUserById(userId: string) {
        const authCredentials: AuthCredentials = {type: JWT, credentials: this.getTokens().access};
        return await this.doFetch<User>(`${this.getUserRoute()}/${userId}`, {}, authCredentials)
    }

    async getUserByUsername(username: string) {
        const authCredentials: AuthCredentials = {type: JWT, credentials: this.getTokens().access};
        return await this.doFetch<User>(`${this.getUserRoute()}/username/${username}`, {}, authCredentials);
    }
}

export const httpClient = new HTTPClient(process.env.REACT_APP_API_BASE_URL!, process.env.REACT_APP_API_VERSION!);
