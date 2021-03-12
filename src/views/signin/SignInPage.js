import {useEffect} from 'react';

import styled, {withTheme} from 'styled-components';

import {SignInForm} from './components/SignInForm';

import {StyledHoverLink} from '../../components/buttons/styles';
import { TopNavbarTransparent } from '../../components/navigation';
import {fontStack, flexCenteredMixin} from '../../components/globals';
import {CenteredLayout} from '../../components/layout/styles';

const SignUpReminder = styled.div`
    ${fontStack};
    ${flexCenteredMixin};
    flex-wrap: wrap;
    padding: 0.5rem;
    margin: 1.5rem 0;
    color: ${props => props.theme.text.white};

    & > p {
        margin-right: 0.3rem;
        font-size: 0.95rem;
    }

    & > a {
        font-size: 0.95rem;
    }
`;

const PageTitle = styled.h1`
    ${fontStack};
    font-weight: 300;
    font-size: 1.75rem;
    margin: 2rem 0;
    color: ${props => props.theme.text.white};
    letter-spacing: 0.03rem;
    text-align: center;

`;

const SignInPage = props => {

    useEffect(() => {
        document.body.title = 'Chatterbox - SignIn'
        document.body.style.backgroundColor = props.theme.bg.primary;
    }, [])
    return (
        <>
            <TopNavbarTransparent linkColor={props.theme.text.white} />
            <CenteredLayout justifyContent='center' alignItems='center'>
                <PageTitle>Sign in to Chatterbox</PageTitle>    
                <SignInForm />
                <SignUpReminder>
                    <p>Don't have an account yet?</p>
                    <StyledHoverLink to='/sign-up' color={props.theme.text.white}>
                        Sign Up
                    </StyledHoverLink>
                </SignUpReminder>
            </CenteredLayout>
        </>
    )
};

export default withTheme(SignInPage);