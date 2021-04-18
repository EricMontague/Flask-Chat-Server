import { AuthInfo } from './types'; 

class LocalStorageClient {

    getItem(key: string) {
        const value = localStorage.getItem(key) || '';
        return value !== '' ? JSON.parse(value) : '';
    }
    
    setItem(key: string, value: any) {
        localStorage.setItem(key, JSON.stringify(value));
    }

    removeItem(key: string) {
        localStorage.removeItem(key);
    }

    getUserCredentials(keys: string[]) {
        const values: string [] = [];
        keys.forEach(key => {
            values.push(this.getItem(key));
        });
        return values;
    }

    setUserCredentials(authInfo: AuthInfo) {
        for (const [key, value] of Object.entries(authInfo)) {
            this.setItem(key, value);
        };
    }

}


export const localStorageClient = new LocalStorageClient();