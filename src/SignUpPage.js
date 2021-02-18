import React from "react";
import Helmet from "react-helmet";
import PropTypes from "prop-types";
import {NavbarTransparent, NavMenu} from "./components/navigation";
import {CenteredFlexLayout} from ".layout";
import {SignUpForm} from "./components/forms";
import {Card, CardBody} from "./card";
import Icon from "./Icon";
import {P, H2} from "./components/globals";
import {FlexRow} from "./components/globals";


const Logo = "styled-component here using Icon component";
const SmallText = "styled-component here using P component";


const SignUpPage = props => {
    return (
        <>
            <Helmet>
                <title>App Name - Sign Up</title>
                <style>{`body {background-color: ${props.theme.bg.primary}; }`}</style>
            </Helmet>
            <NavbarTransparent>
                <FlexRow>
                    <Logo />
                    <NavMenu />
                </FlexRow>
            </NavbarTransparent>
            <CenteredFlexLayout>
                <H2>Create your account</H2>
                <Card>
                    <CardBody>
                        <SignUpForm />
                    </CardBody>
                </Card>
                
            </CenteredFlexLayout>
        </>
    )
};

export default SignUpPage;