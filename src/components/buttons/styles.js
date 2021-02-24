import styled from "styled-components";
import {flexCenteredMixin, fontStack} from "../globals";
import { Link } from "react-router-dom";

// https://www.hexcolortool.com/#a5222b


export const StyledLink = styled(Link)`
    ${fontStack};
    display: flex;
    align-items: center;
    flex: none;
    color: ${props => props.color || props.theme.text.default};

    &:focus {
        outline: none;
    }
`;


export const StyledHoverLink = styled(StyledLink)`
    transition: opacity 0.2s ease-in-out;
    
    &:hover {
        opacity: 0.85;
    }
`;


export const StyledButton = styled.button`
    ${flexCenteredMixin}
    flex: none;
    font-size: 1rem;
    font-weight: 500;
    border: 0;
    color: ${props => props.theme.text.default};
    background: ${props => props.theme.bg.light};
    cursor: ${props => props.disabled ? "default" : "pointer"};
    padding: ${props => props.padding || "0.7rem 1rem"};
    border-radius: 0.25rem;
    opacity: ${props => props.disabled ? "0.6" : "1"};
    line-height: 1.2;
    width: ${props => props.width || "auto"};
    transition: background, color 0.3s ease-in-out;

    &:focus {
        outline: none;
    }
`;


export const StyledPrimaryButton = styled(StyledButton)`
    color: ${props => props.theme.text.white};
    background: ${props => props.theme.bg.primary};
    
    &:hover {
        background:  #0a46e4;
    }

    &:active {
        background: #0039d7;
    }
`;


export const StyledWarnButton = styled(StyledButton)`
    color: ${props => props.theme.text.white};
    background: ${props => props.theme.bg.warn};

    &:hover {
        background: #ba2630;
    }

    &active {
        background: #a5222b;
    }
`;


export const StyledOutlineButton = styled(StyledButton)`
    color: ${props => props.theme.text.white};
    background: transparent;
    border: 1px solid ${props => props.theme.text.white}; 
`;


export const StyledHoverOutlineButton = styled(StyledOutlineButton)`
    transition: all 0.3s ease-in-out;

    &:hover {
        color: #263543;
        background: ${props => props.theme.bg.default};
    }
`;

export const StyledPrimaryOutlineButton = styled(StyledOutlineButton)`
    color: ${props => props.theme.text.primary};
    border: 1px solid ${props => props.theme.text.primary};
`;

