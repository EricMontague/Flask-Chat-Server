import React from 'react';
import {
    BrowserRouter as Router,
    Switch,
    Route
} from 'react-router-dom';
import { ThemeProvider } from 'styled-components';
import theme from '../common/theme';
import SignInController from '../features/signin/SignInController';
import SignUpController from '../features/signup/SignUpController';
import GlobalStyle from '../globalStyle';

const App = () => {
    return (
        <Router>
            <ThemeProvider theme= { theme }>
                <GlobalStyle />
                <Switch>
                    <Route exact path='/sign-in' >
                        <SignInController />
                    </Route>
                    <Route exact path='/sign-up'>
                        <SignUpController />
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