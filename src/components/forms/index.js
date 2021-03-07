import React from "react";
import PropTypes from "prop-types";
import {Formik} from "formik";
import * as Yup from "yup";
import {StyledCard, StyledCardBody} from "../cards/styles";
import {StyledFormikForm} from "./styles";
import {TextInput, InputError} from "../formElements";
import AutocompleteInput from "../formElements/AutocompleteInput";
import {PrimaryButton} from "../buttons";
import {GOOGLE_PLACES_API_TYPES, GOOGLE_PLACES_API_FIELDS, GOOGLE_PLACES_API_COUNTRIES} from "../../constants";


const validationSchema = Yup.object({
    username: Yup.string().required().min(2).max(32),
    name: Yup.string().required().min(2).max(32),
    email: Yup.string().required().email().min(5).max(32),
    password: Yup.string().required().min(12).max(32)
});


export const SignUpForm = props => {

    const isFormCompleted = values => {
        for (const field in values) {
            if (values[field] === "") {
                return false;
            }
        }
        return true;
    }

    const handleAutocompleteChange = (setFieldValue, fieldName) => {

        const onChange = (value, action) => {
            setFieldValue(fieldName, value, false);
        };

        return onChange;
        
    };

    const handleSubmit = (values, actions) => {
        console.log(values);
        console.log(actions);
        const formValues = {
            ...values,
            location: values.location.label
        }
        actions.setSubmitting(false);
        // actions.resetForm();
    }

    
    return (
        <Formik
            initialValues={{
                username: "",
                name: "",
                email: "",
                password: "",
                location: ""
            }}
            validationSchema={validationSchema}
            onSubmit={handleSubmit}
        >
            {({values, setFieldValue, isSubmitting, isValid}) => (
                <StyledCard maxWidth="30rem">
                    <StyledCardBody>
                        <StyledFormikForm>
                            
                            <TextInput placeholder="Username" name="username"/>
                            <InputError name="username" />
                               
                            <TextInput placeholder="Name" name="name"/>
                            <InputError name="name" />

                            <TextInput placeholder="Email" name="email"/>
                            <InputError name="email" />
      
                            <TextInput placeholder="Choose password" name="password" type="password"/>
                            <InputError name="password" />

                            <AutocompleteInput 
                                handleChange={handleAutocompleteChange(setFieldValue, "location")}
                                types={GOOGLE_PLACES_API_TYPES}
                                fields={GOOGLE_PLACES_API_FIELDS}
                                name="location"
                                value={values.location}
                                validCountries={GOOGLE_PLACES_API_COUNTRIES}
                            />
                            
                            <PrimaryButton 
                                disabled={!isValid || !isFormCompleted(values) || isSubmitting} 
                                width="100%" 
                                padding="1.5rem" 
                                type="submit"
                            >
                                Create account
                            </PrimaryButton>
                        </StyledFormikForm>
                    </StyledCardBody>
                </StyledCard>
            )}
        </Formik>
    );
};

