import { createSlice, PayloadAction, createEntityAdapter, EntityState, createAsyncThunk } from '@reduxjs/toolkit';
import { RootState } from '../../app/store';
import { httpClient } from '../../clients/httpClient';

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

interface Tokens {
    access: string; 
    refresh: string; 
};

interface User {
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
};

interface LoginInfo {
    email: string;
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
    currentUserId: 'user_id1',
    tokens: {access: "access_token", refresh: "refresh_token"},
    ids: ['user_id1'],
    entities: {
        user_id1: {
            id: 'user_id1',
            name: 'Brad',
            username: 'Brad345',
            email: 'brad@gmail.com',
            joined_on: '2021-04-07T18:42:56.645783',
            last_seen_at: '2021-04-07T18:42:56.645783',
            password: 'password',
            bio: 'I am groot!',
            resource_type: 'User',
            location: {city: 'New York', state: 'New York', country: 'United States'},
            avatar: {url: 'https://www.example.com', width: 400, height: 400},
            cover_photo: {url: 'https://www.example.com', width: 400, height: 400}
        }
    }
    
});

export const login = createAsyncThunk(
    'users/login',
    async (loginInfo: LoginInfo, thunkAPI) => {
        const response = await httpClient.login(loginInfo.email, loginInfo.password);
        return response.tokens;
    };
);

export const register = createAsyncThunk(
    'users/register',
    async (registrationInfo: RegistrationInfo, thunkAPI) => {
        const response = await httpClient.register(registrationInfo);
        return response.user;
    };
);

export const usersSlice = createSlice({
    name: 'users',
    initialState,
    reducers: {
        login(state, action: PayloadAction<Tokens>) {
            state.tokens = action.payload;
        },
        register(state, action: PayloadAction<User>) {
            state.currentUserId = action.payload.id;
            state.entities[action.payload.id] = action.payload;
            state.ids.push(action.payload.id);
        }
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

export default usersSlice.reducer;