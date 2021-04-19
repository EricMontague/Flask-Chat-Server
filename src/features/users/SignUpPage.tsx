import React, { useEffect } from 'react';
import PropTypes from 'prop-types';
import { useHistory } from 'react-router-dom';
import styled, { withTheme, DefaultTheme } from 'styled-components';
import { StyledHoverLink } from '../../common/components/buttons/styles';
import { TopNavbarTransparent } from '../../common/components/navigation';
import { SignUpForm } from './SignUpForm';
import { fontStack, flexCenteredMixin } from '../../common/components/globals';
import { StyledCenteredLayout } from '../../common/components/layout/styles';
import { getCurrentUser } from './usersSlice';
import { useAppSelector } from '../../app/hooks';

type Props = {
    theme: DefaultTheme;
};

const SignUpReminder = styled.div`
    ${fontStack};
    ${flexCenteredMixin};
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

const SignUpPage = (props: Props) => {

    const history = useHistory();

    const currentUser = useAppSelector(getCurrentUser);
    
    useEffect(() => {
        document.title = 'ChatterBox - Sign Up';
        document.body.style.backgroundColor = props.theme.bg.primary;
        if (currentUser) {
            console.log('CurrentUser stored in Redux state');
            history.push('/');
        };
    }, [])

       
    return (
        <>
            <TopNavbarTransparent linkColor={props.theme.text.white}/>
            <StyledCenteredLayout justifyContent='center' alignItems='center'>
                <PageTitle>Create your account</PageTitle>    
                <SignUpForm />
                <SignUpReminder>
                    <p>Already have an account?</p>
                    <StyledHoverLink to='/sign-in' color={props.theme.text.white}>
                        Sign In
                    </StyledHoverLink>
                </SignUpReminder>
            </StyledCenteredLayout>
        </>
    )
};

SignUpPage.propTypes = {
    theme: PropTypes.objectOf(PropTypes.objectOf(PropTypes.string.isRequired).isRequired).isRequired
}

export default withTheme(SignUpPage);