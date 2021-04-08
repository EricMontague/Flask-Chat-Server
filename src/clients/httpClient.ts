import { authClient } from './authClient';
import { RegistrationInfo } from '../features/users/usersSlice';
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

        Object.defineProperty(this, 'message', {enumerable: true});
    }

};

class HTTPClient {

    baseUrl: string;
    logToConsole: boolean;

    constructor(authClient, baseUrl: string) {
        this.authClient = authClient;
        this.baseUrl = baseUrl;
        this.logToConsole = process.env.REACT_APP_LOG_TO_CONSOLE === 'true';

    }

    doFetch = async <T>(url: string, options: FetchOptions): Promise<T> => {
        const {data} = await this.doFetchWithResponse<T>(url, options);
        return data;
    };

    doFetchWithResponse = async <T>(url: string, options: FetchOptions): Promise<ClientResponse<T>> => {
        const response = await fetch(url, this.getOptions(options));

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

    getOptions(options: FetchOptions) {
        
    }

    login(email: string, password: string) {

    }

    registration(registrationInfo: RegistrationInfo) {

    }
}


export const httpClient = HttpClient(authClient)
