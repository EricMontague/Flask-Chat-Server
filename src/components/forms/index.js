import React from "react";
import {useFormik} from "formik";
import {StyledCard, StyledCardBody} from "../cards/styles";
import {StyledForm} from "./styles";
import {Input} from "../formElements";
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

    
    return (
        <StyledCard maxWidth="30rem">
            <StyledCardBody>
                <Formik
                    initialValues={{
                        username: "",
                        name: "",
                        email: "",
                        password: ""
                    }}
                    onSubmit={(values, {setSubmitting}) => {
                        console.log(values);
                        setSubmitting(false);
                    }}
                >
                    {({
                        values,
                        handleChange,
                        handleSubmit,
                        isSubmitting
                    }) => (
                        <StyledForm onSubmit={handleSubmit}>
                            <StyledInputRow>
                                <Input
                                    id="username" 
                                    type="text" 
                                    placeholder="Username"
                                    name="username"
                                    value={values.username}
                                    withLabel={false}
                                    handleChange={handleChange}
                                />
                                <Input
                                    id="name"
                                    type="text" 
                                    placeholder="Name"
                                    name="name"
                                    value={values.name}
                                    withLabel={false}
                                    handleChange={handleChange}
                                />
                            </StyledInputRow>
                            <StyledInputRow>
                                <Input
                                    id="email"
                                    type="text" 
                                    placeholder="Email"
                                    name="email"
                                    value={values.email}
                                    withLabel={false}
                                    handleChange={handleChange}
                                />
                            </StyledInputRow>
                            <StyledInputRow>
                                <Input
                                    id="password"
                                    type="password" 
                                    placeholder="Choose password"
                                    name="password"
                                    value={values.password}
                                    withLabel={false}
                                    handleChange={handleChange}
                                />
                            </StyledInputRow>
                            {/* <LocationField /> */}
                            <PrimaryButton disabled={!isFormCompleted(values)} width="100%" padding="1.5rem" type="submit">
                                Create account
                            </PrimaryButton>
                        </StyledForm>
                    )}
                </Formik>
            </StyledCardBody>
        </StyledCard>
    );
    
    
};

