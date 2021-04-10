import React, { useEffect } from 'react';
import {
    BrowserRouter as Router,
    Switch,
    Route
} from 'react-router-dom';
import { ThemeProvider } from 'styled-components';
import theme from '../common/theme';
import SignInPage from '../features/users/SignInPage';
import SignUpPage from '../features/users/SignUpPage';
import GlobalStyle from '../globalStyle';
import { loadUser } from '../features/usersSlice';
import { useAppDispatch } from './hooks';

const App = () => {

    const dispatch = useAppDispatch();
    
    useEffect(() => {
        dispatch(loadUser());
    }, [])
    
    return (
        <Router>
            <ThemeProvider theme= { theme }>
                <GlobalStyle />
                <Switch>
                    <Route exact path='/sign-in' >
                        <SignInPage />
                    </Route>
                    <Route exact path='/sign-up'>
                        <SignUpPage />
                    </Route>
                    <Route exact path='/'>
                        <h1>Hello, World!</h1>
                    </Route>
                    <Route path='*'>
                        <h1>Page does not Exist!</h1>
                    </Route>
                </Switch>
            </ThemeProvider>
        </Router>
    )
};

export default App;