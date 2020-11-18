import { createGlobalStyle } from "styled-components";
import theme from "./theme"


const ResetStyle = createGlobalStyle`

    * {
        box-sizing: border-box;
        margin: 0;
        padding: 0;
    }

    body {
        background-color: ${theme.bg.default};
        font-family: ${theme.font.default};
        line-height: 1.6;
        color: ${theme.text.default}
    }

    a {
        text-decoration: none;
    }

    a:hover {
        cursor: pointer;
    }

    ul {
        list-style: none;
    }

`;


export default ResetStyle;