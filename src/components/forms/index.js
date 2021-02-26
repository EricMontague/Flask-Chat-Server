import React from "react";
import {Formik} from "formik";
import * as Yup from "yup";
import {StyledCard, StyledCardBody} from "../cards/styles";
import {StyledFormikForm} from "./styles";
import {TextInput} from "../formElements";
import {StyledInputRow} from "../formElements/styles";
import {PrimaryButton} from "../buttons";


export const SignUpForm = props => {

    const isFormCompleted = values => {
        for (const field in values) {
            if (values[field] === "") {
                return false;
            }
        }
        return true;
    }

    const handleSubmit = (values, actions) => {
        console.log(values.username);
        actions.setSubmitting(false);
    }

    
    return (
        <Formik
            initialValues={{
                username: "",
                name: "",
                email: "",
                password: ""
            }}
            validationSchema={
                Yup.object({
                username: Yup.string().required().min(2).max(32),
                name: Yup.string().required().min(2).max(32),
                email: Yup.string().required().email().min(5).max(32),
                password: Yup.string().required().min(12).max(32)
            })}
            onSubmit={handleSubmit}
        >
            {({values, isSubmitting}) => (
                <StyledCard maxWidth="30rem">
                    <StyledCardBody>
                        <StyledFormikForm>
                            <StyledInputRow>
                                <TextInput
                                    placeholder="Username"
                                    name="username"
                                />
                                <TextInput
                                    placeholder="Name"
                                    name="name"
                                />
                            </StyledInputRow>
                            <StyledInputRow>
                                <TextInput
                                    placeholder="Email"
                                    name="email"
                                />
                            </StyledInputRow>
                            <StyledInputRow>
                                <TextInput
                                    placeholder="Choose password"
                                    name="password"
                                />
                            </StyledInputRow>
                            {/* <LocationField /> */}
                            <PrimaryButton disabled={!isFormCompleted(values) || isSubmitting} width="100%" padding="1.5rem" type="submit">
                                Create account
                            </PrimaryButton>
                        </StyledFormikForm>
                    </StyledCardBody>
                </StyledCard>
            )}
        </Formik>
    );
    
    
};

