import React from "react";
import PropTypes from "prop-types";
import {Formik} from "formik";
import * as Yup from "yup";
import {StyledCard, StyledCardBody} from "../cards/styles";
import {StyledFormikForm} from "./styles";
import {TextInput, InputError} from "../formElements";
import AutocompleteInput from "../formElements/AutocompleteInput";
import {StyledInputRow} from "../formElements/styles";
import {PrimaryButton} from "../buttons";
import {FlexCol} from "../globals";



export const SignUpForm = props => {

    const isFormCompleted = values => {
        for (const field in values) {
            if (values[field] === "") {
                return false;
            }
        }
        return true;
    }

    const hasErrors = errors => {
        for (const field in errors) {
            if (errors[field] !== "") {
                return true;
            }
        }
        return false;
    };

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
            {({values, errors, isSubmitting}) => (
                <StyledCard maxWidth="30rem">
                    <StyledCardBody>
                        <StyledFormikForm>
                            <StyledInputRow>
                                <FlexCol>
                                    <TextInput
                                        placeholder="Username"
                                        name="username"
                                    />
                                    <InputError name="username" />
                                </FlexCol>
                                <FlexCol>
                                    <TextInput
                                        placeholder="Name"
                                        name="name"
                                    />
                                    <InputError name="name" />
                                </FlexCol>
                            </StyledInputRow>
                            
                            <StyledInputRow>
                                <TextInput
                                    placeholder="Email"
                                    name="email"
                                />
                            </StyledInputRow>
                            <InputError name="email" />
                            <StyledInputRow>
                                <TextInput
                                    placeholder="Choose password"
                                    name="password"
                                />
                            </StyledInputRow>
                            <InputError name="password" />
                            <AutocompleteInput />
                            <PrimaryButton disabled={hasErrors(errors) || !isFormCompleted(values) || isSubmitting} width="100%" padding="1.5rem" type="submit">
                                Create account
                            </PrimaryButton>
                        </StyledFormikForm>
                    </StyledCardBody>
                </StyledCard>
            )}
        </Formik>
    );
};

