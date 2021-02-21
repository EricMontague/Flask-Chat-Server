import React from "react";
import Helmet from "react-helmet";
import {StyledLink} from "./components/buttons/styles";
import styled from "styled-components";
import PropTypes from "prop-types";
import {NavbarTransparent, NavMenu} from "./components/navigation";
import {CenteredFlexLayout} from ".layout";
import {SignUpForm} from "./components/forms";
import Card from ".components/cards";
import {P, H2, FlexRow} from "./components/globals";
import {FlexRow} from "./components/globals";


const Logo = styled(StyledLink)`
    color: ${props => props.color ? props.color : props.theme.text.default};
    font-weight: 600;
`;


const FinePrint = styled(P)`
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 0.5rem;
    margin: 1rem 0;
    color: ${props => props.theme.text.default};
`;


const SignUpPage = props => {
    return (
        <>
            <Helmet>
                <title>App Name - Sign Up</title>
                <style>{`body {background-color: ${props.theme.bg.primary}; }`}</style>
            </Helmet>
            <NavbarTransparent>
                <FlexRow>
                    <Logo to={"/"}>TalkChat</Logo>
                    <NavMenu />
                </FlexRow>
            </NavbarTransparent>
            <CenteredFlexLayout>
                <H2>Create your account</H2>
                <Card>
                    <Card.Body>
                        <SignUpForm />
                    </Card.Body>
                </Card>
                <FinePrint>
                    Already have an account? 
                    <StyledLink to="/sign-in">
                        Sign In
                    </StyledLink>
                </FinePrint>
            </CenteredFlexLayout>
        </>
    )
};

export default SignUpPage;