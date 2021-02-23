import styled from "styled-components";
import { Link } from "react-router-dom";

// https://www.hexcolortool.com/#a5222b


export const StyledLink = styled(Link)`
    display: flex;
    align-items: center;
    flex: none;
`;


export const StyledButton = styled.button`
    display: flex;
    justify-content: center;
    align-items: center;
    flex: none;
    font-size: 1rem;
    border: 0;
    color: ${props => props.theme.text.default};
    background: ${props => props.theme.bg.light};
    cursor: pointer;
    padding: ${props => props.padding || "0.75rem 1rem"};
    border-radius: 0.25rem;
    opacity: ${props => props.disabled ? "0.6" : "1"}
    line-height: 1.2;
    width: ${props => props.width || "auto"};
    transition: background, color 0.3s ease-in-out;
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

    &:hover {
        color: #263543;
        background: ${props => props.theme.bg.default};
    }
`;

export const StyledPrimaryOutlineButton = styled(StyledOutlineButton)`
    color: ${props => props.theme.text.primary};
    border: 1px solid ${props => props.theme.text.primary};
`;

