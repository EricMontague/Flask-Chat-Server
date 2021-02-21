import styled from "styled-components";
import {zIndex} from "../globals";


export const StyledLabel = styled.label`
    color: ${props => props.theme.text.default};
    margin-top: 0.75rem;
    z-index: ${zIndex.formElement};
`;


export const StyledInput = styled.input`
    border: 1px solid #edeff1;
    border-radius: 0.25rem;
    background: ${props => props.theme.bg.default};
    padding: 0.5rem 1rem;
    margin-top: 0.5rem;
    margin-bottom: 0.5rem;
    transition: border-color 0.3s ease-in-out;
    z-index: ${zIndex.formElement};

    &:focus {
        border-color: #52a8ec;
    }
`;

