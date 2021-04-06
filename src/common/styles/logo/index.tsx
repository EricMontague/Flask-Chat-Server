import React from 'react';
import styled from 'styled-components';
import {MessageSquare} from 'react-feather';
import {StyledLink} from '../buttons/styles';
import {fontStack, media} from '../globals';

const LogoIcon = styled(MessageSquare)`
    margin-right: 0.25rem;
    color= ${props => props.theme.text.default}
`;

const LogoContainer = styled(StyledLink)`
    ${fontStack};
    letter-spacing: 0.03rem;
    color: ${props => props.theme.text.white};
    font-weight: 500;
    font-size: 1.4rem;

    span {
        padding-bottom: 0.25rem;
    }

    ${media.small} {
        font-size: 1.2rem;
    }
`;

export const WhiteLogo = () => {
    return (
        <LogoContainer to={'/'}>
            <LogoIcon />
            <span>ChatterBox</span>
        </LogoContainer>
    );
};


