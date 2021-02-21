import React from "react";
import {
    BrowserRouter as Router,
    Switch,
    Route
} from "react-router-dom";
import { ThemeProvider } from "styled-components";
import theme from "./theme";
import SignInPage from "./pages/SignInPage";
import SignUpPage from "./pages/SignUpPage";
import GlobalStyle from "./globalStyle";



const App = () => {
    return (
        <Router>
            <ThemeProvider theme= { theme }>
                <GlobalStyle />
                <Switch>
                    <Route exact path="/sign-in" >
                        <SignInPage />
                    </Route>
                    <Route exact path="/sign-up">
                        <SignUpPage />
                    </Route>
                    <Route exact path="/">
                        <h1>Hello, World!</h1>
                    </Route>
                </Switch>
            </ThemeProvider>
        </Router>
    )
};


export default App;