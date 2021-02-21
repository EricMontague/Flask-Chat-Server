import { createGlobalStyle } from "styled-components";
import theme from "./theme"


const GlobalStyle = createGlobalStyle`

    * {
        box-sizing: border-box;
        margin: 0;
        padding: 0;
        -webkit-font-smoothing: auto;
        font-weight: inherit;
        -webkit-appearance: none;
        -moz-appearance: none;
    }

    html {
        font-size: 16px;
        
    }

    body {
        -webkit-overflow-scrolling: touch;
        overscroll-behavior-y: none;
        color: ${theme.text.default}
        line-height: 1.5;
        font-family: ${theme.font.default};
        background-color: ${theme.bg.default};
    }

    a {
        text-decoration: none;
        color: ${theme.text.default};
    }

    a:hover {
        cursor: pointer;
    }

    ul {
        list-style: none;
    }

`;


export default GlobalStyle;