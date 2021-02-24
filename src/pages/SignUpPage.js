import React from "react";
import Helmet from "react-helmet";
import {StyledLink, StyledHoverLink} from "../components/buttons/styles";
import {OutlineButton} from "../components/buttons";
import styled, {withTheme} from "styled-components";
import PropTypes from "prop-types";
import {StyledNavbarTransparent, StyledNavbarMenu, StyledNavbarMenuItem} from "../components/navigation";
import {SignUpForm} from "../components/forms";
import {fontStack, flexCenteredMixin, FlexRow, FlexCol} from "../components/globals";


const Logo = styled(StyledLink)`
    ${fontStack};
    flex: 1 0 auto;
    letter-spacing: 0.03rem;
    color: ${props => props.theme.text.white};
    font-weight: 600;
    font-size: 1.5rem;
`;


const SignInReminder = styled.div`
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
    margin-bottom: 2rem;
    color: ${props => props.theme.text.white};
    letter-spacing: 0.03rem;
`;


const SignUpPage = props => {
    return (
        <>
            <Helmet>
                <title>App Name - Sign Up</title>
                <style type="text/css">{`
                    body {
                        background-color: ${props.theme.bg.primary};
                    }
                `}</style>
            </Helmet>
            <StyledNavbarTransparent>
                <FlexRow>
                    <Logo to={"/"}>TalkChat</Logo>
                    <StyledNavbarMenu justifyContent="flex-end">
                        <StyledNavbarMenuItem>
                            <StyledHoverLink to="/sign-in" color={props.theme.text.white}>
                                Sign In
                            </StyledHoverLink>
                        </StyledNavbarMenuItem>
                        <StyledNavbarMenuItem>
                            <OutlineButton to="/sign-up">Sign Up</OutlineButton>
                        </StyledNavbarMenuItem>
                    </StyledNavbarMenu>
                </FlexRow>
            </StyledNavbarTransparent>
            <FlexCol justifyContent="center" alignItems="center">
                <PageTitle>Create your account</PageTitle>    
                <SignUpForm />
                <SignInReminder>
                    <p>Already have an account?</p>
                    <StyledHoverLink to="/sign-in" color={props.theme.text.white}>
                        Sign In
                    </StyledHoverLink>
                </SignInReminder>
            </FlexCol>
        </>
    )
};

export default withTheme(SignUpPage);