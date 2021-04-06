import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { RootState } from '../../app/store';

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

interface UserState {
    currentUserId: string;
    tokens: {access: string, refresh: string};
    users: User [];
};

const initialState: Partial<UserState> = {
    currentUserId: 'aef',
    tokens = {access: "aef", refresh: "aef"},
    users: [
        {
            id: 'aef',
            username: 'Brad',
            email: 'brad@gmail.com',
            joined_on: '',
            last_seen_at: '',
            password: 'password',
            bio: 'I am groot!',
            resource_type: 'User',
            location: {city: 'New York', state: 'New York', country: 'United States'},
            avatar: {url: 'https://www.example.com', width: 400, height: 400},
            cover_photo: {url: 'https://www.example.com', width: 400, height: 400}
        }
    ]
    
};

export const usersSlice = createSlice({
    name: 'users',
    initialState,
    reducers: {
        changeUsername: (state, action: PayloadAction<string>) => {
            state.username = action.payload;
        }
    }
})

export const { changeUsername } = usersSlice.actions;


export default usersSlice.reducer;