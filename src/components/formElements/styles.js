import styled from "styled-components";
import {zIndex, FlexRow} from "../globals";


export const StyledLabel = styled.label`
    color: ${props => props.theme.text.default};
    margin-bottom: 0.75rem;
    z-index: ${zIndex.formElement};
`;


export const StyledInput = styled.input`
    flex: 1 0 auto;
    border: none;
    border-radius: 0.25rem;
    background: none;
    font-size: 1rem;
    padding: 1.25rem;
    width: 100%;
    color ${props => props.theme.text.default};
    

    &:focus {
        outline: none;
    }

    &::placeholder{
        color: ${props => props.theme.input.placeholder};
        letter-spacing: 0.03rem;
    }
`;


export const StyledInputContainer = styled(FlexRow)`
    flex: 1 1 auto;
    position: relative;
    margin-bottom: 1rem;
    border-radius: 0.25rem;
    border: 1px solid ${props => props.theme.input.border};
    background: ${props => props.theme.bg.default};
    transition: all 0.25s ease;
    z-index: ${zIndex.formElement};

    &:hover {
        border-color: #e0e3e5;
    }

    &:focus-within {
        border-color: ${props => props.theme.bg.primary};
    }

    
`;

