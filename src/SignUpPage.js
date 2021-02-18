import React from "react";
import Helmet from "react-helmet";
import PropTypes from "prop-types";
import {NavbarTransparent, NavMenu} from "./components/navigation";
import {CenteredFlexLayout} from ".layout";
import InputField from "./InputField";
import {PrimaryButton} from "./button";
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
                        <form method="POST" action={`${window.location.href}/auth/register`}>
                            <InputField type="text" placeholder="Username"/>
                            <InputField type="text" placeholder="Name"/>
                            <InputField type="text" placeholder="Email"/>
                            <InputField type="password" placeholder="Password"/>
                            {/* <LocationField /> */}
                            <PrimaryButton type="submit">Create account</PrimaryButton>
                        </form>
                    </CardBody>
                </Card>
                
            </CenteredFlexLayout>
        </>
    )
};

export default SignUpPage;