import { createSlice, createEntityAdapter, EntityState, createAsyncThunk } from '@reduxjs/toolkit';
import { RootState } from '../../app/store';
import { httpClient } from '../../clients/httpClient';
import { localStorageClient } from '../../clients/storageClient';
import { ACCESS_TOKEN, REFRESH_TOKEN } from '../../constants';

export const USER_REQUEST_IDLE = 'idle';
export const USER_REQUEST_LOADING = 'loading';
export const USER_REQUEST_SUCCEEDED = 'succeeded';
export const USER_REQUEST_FAILED = 'failed';

interface Location {
    city: string;
    state: string;
    country: string;
};

interface Image {
    url: string;
    width: number;
    height: number;
};

export interface Tokens {
    access: string; 
    refresh: string; 
};

export interface User {
    id: string;
    username: string;
    name: string;
    email: string;
    joined_on: string;
    last_seen_at: string;
    password: string;
    bio: string;
    resource_type: string;
    location: Location;
    avatar: Image;
    cover_photo: Image;
};

interface UsersState extends EntityState<User> {
    currentUserId: string;
    tokens: Tokens;
    status: 'idle' | 'loading' | 'succeeded' | 'failed';
    error?: string;
};

interface LoginInfo {
    username: string;
    password: string;
};

export interface RegistrationInfo {
    username: string;
    name: string;
    email: string;
    password: string;
    location: Location;
};

const usersAdapter = createEntityAdapter<User>();

const initialState: UsersState = usersAdapter.getInitialState({
    currentUserId: '',
    tokens: {access: "", refresh: ""},
    status: 'idle',
    error: undefined,
    ids: [],
    entities: {}
});

// TODO - Optimize so that a call to get the user by username is only made if the currentUserId
// is not already set in the Redux state
export const login = createAsyncThunk(
    'users/login',
    async (loginInfo: LoginInfo, thunkAPI) => {
        const tokens = await httpClient.login(loginInfo.username, loginInfo.password);
        const currentUser = await httpClient.getUserByUsername(loginInfo.username);
        localStorageClient.setUserCredentials({
            [ACCESS_TOKEN]: tokens.access,
            [REFRESH_TOKEN]: tokens.refresh,
            'username': loginInfo.username
        });
        return {tokens, currentUser};
    }
);

export const register = createAsyncThunk(
    'users/register',
    async (registrationInfo: RegistrationInfo, thunkAPI) => {
        return await httpClient.register(registrationInfo);
    }
);

export const loadUser = createAsyncThunk(
    'users/load_user',
    async (thunkAPI) => {
        const [ access, refresh, username ] = localStorageClient.getUserCredentials([
            ACCESS_TOKEN, REFRESH_TOKEN, 'username'
        ]);
        httpClient.setTokens({access, refresh});
        const currentUser = await httpClient.getUserByUsername(username);
        return {
            currentUser,
            tokens: {access, refresh}
        }
    }
);

export const usersSlice = createSlice({
    name: 'users',
    initialState,
    reducers: {},
    extraReducers: (builder) => {
        builder
            .addCase(login.pending, (state) => {
                state.status = USER_REQUEST_LOADING;
            })
            .addCase(login.fulfilled, (state, action) => {
                const { tokens, currentUser } = action.payload;
                state.tokens = tokens;
                state.currentUserId = currentUser.id;
                state.ids.push(currentUser.id);
                state.entities[currentUser.id] = currentUser;
                state.status = USER_REQUEST_SUCCEEDED;
            })
            .addCase(login.rejected, (state, action) => {
                state.status = USER_REQUEST_FAILED;
                state.error = action.error.message;
            })
            .addCase(register.pending, (state) => {
                state.status = USER_REQUEST_LOADING;
            })
            .addCase(register.fulfilled, (state, action) => {
                state.currentUserId = action.payload.id;
                state.entities[action.payload.id] = action.payload;
                state.ids.push(action.payload.id);
                state.status = USER_REQUEST_SUCCEEDED;
            })
            .addCase(register.rejected, (state, action) => {
                state.status = USER_REQUEST_FAILED;
                state.error = action.error.message;
            })
            .addCase(loadUser.pending, (state) => {
                state.status = USER_REQUEST_LOADING;;
            })
            .addCase(loadUser.fulfilled, (state, action) => {
                const { currentUser, tokens } = action.payload;
                state.tokens = tokens;
                state.currentUserId = currentUser.id;
                state.entities[currentUser.id] = currentUser;
                state.ids.push(currentUser.id);
                state.status = USER_REQUEST_SUCCEEDED;
            })
            .addCase(loadUser.rejected, (state, action) => {
                state.status = USER_REQUEST_FAILED;
                state.error = action.error.message;
            })
    }   
});

export const {
    selectAll: selectAllUsers,
    selectById: selectUserById,
    selectIds: selectUserIds
} = usersAdapter.getSelectors((state: RootState) => state.users);

export const getCurrentUser = (state: RootState) => {
    if (state.users.currentUserId in state.users.entities) {
        return state.users.entities[state.users.currentUserId];
    }
    return null;
};

export const getUserTokens = (state: RootState) => state.users.tokens;

export default usersSlice.reducer;


// currentUserId: 'user_id1',
//     tokens: {access: "access_token", refresh: "refresh_token"},
//     status: 'idle',
//     error: undefined,
//     ids: ['user_id1'],
//     entities: {
//         user_id1: {
//             id: 'user_id1',
//             name: 'Brad',
//             username: 'Brad345',
//             email: 'brad@gmail.com',
//             joined_on: '2021-04-07T18:42:56.645783',
//             last_seen_at: '2021-04-07T18:42:56.645783',
//             password: 'password',
//             bio: 'I am groot!',
//             resource_type: 'User',
//             location: {city: 'New York', state: 'New York', country: 'United States'},
//             avatar: {url: 'https://www.example.com', width: 400, height: 400},
//             cover_photo: {url: 'https://www.example.com', width: 400, height: 400}
//         }
//     }