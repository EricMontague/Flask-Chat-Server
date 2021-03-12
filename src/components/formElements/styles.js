import styled from 'styled-components';
import {zIndex, FlexRow, Span} from '../globals';


export const StyledLabel = styled.label`
    display: inline-block;
    color: #333;
    padding-bottom: 0.75rem;
    z-index: ${zIndex.formElement};
`;


export const StyledInput = styled.input`
    flex: 1 1 auto;
    width: 100%;
    border: 1px solid ${props => props.theme.input.border};
    border-radius: 0.25rem;
    background: ${props => props.theme.bg.default};
    font-size: 1rem;
    padding: 1.25rem;
    color ${props => props.theme.text.default};
    transition: all 0.25s ease;
    

    &:hover {
        border: 1px solid ${props => props.theme.input.borderHover};
    }

    &:focus {
        outline: none;
        border-color: ${props => props.theme.bg.primary};
    }

    &::placeholder{
        color: ${props => props.theme.input.placeholder};
        letter-spacing: 0.03rem;
    }

    
`;


export const StyledInputContainer = styled.div`
    flex: 1 1 auto%;
    width: 100%;
    position: relative;
    margin-bottom: 1rem;
    z-index: ${zIndex.formElement};    
`;


export const StyledInputRow = styled(FlexRow)`
    & > *:not(:first-child) {
        margin-left: 1rem;
    }
`;



export const StyledErrorMessage = styled(Span)`
    flex: 1 1 100%;
    color: ${props => props.theme.text.warn};
    margin-bottom: 1rem;
`;

