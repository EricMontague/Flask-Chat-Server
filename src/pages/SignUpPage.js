import {useEffect} from "react";
import PropTypes from "prop-types";
import styled, {withTheme} from "styled-components";
import {StyledHoverLink} from "../components/buttons/styles";
import {TopNavbarTransparent} from "../components/navigation";
import {SignUpForm} from "../components/forms";
import {fontStack, flexCenteredMixin, FlexCol} from "../components/globals";



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
    margin: 2rem 0;
    color: ${props => props.theme.text.white};
    letter-spacing: 0.03rem;
`;


const SignUpPage = props => {

    useEffect(() => {
        document.title = "ChatterBox - Sign Up";
        document.body.style.backgroundColor = props.theme.bg.primary;
    }, [])
    return (
        <>
            <TopNavbarTransparent linkColor={props.theme.text.white}/>
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