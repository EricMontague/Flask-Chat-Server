import React from 'react';
import {Formik, FormikHelpers} from 'formik';
import * as Yup from 'yup';
import { OptionTypeBase, ActionMeta } from 'react-select';
import {StyledCard, StyledCardBody} from '../../../components/cards/styles';
import {StyledFormikForm} from '../../../components/forms/styles';
import {TextInput} from '../../../components/formElements/TextInput';
import {InputError} from '../../../components/formElements/InputError';
import AutocompleteInput from '../../../components/formElements/AutocompleteInput';
import {PrimaryButton} from '../../../components/buttons';
import {GOOGLE_PLACES_API_TYPES, GOOGLE_PLACES_API_FIELDS, GOOGLE_PLACES_API_COUNTRIES} from '../../../constants';

type FormValues = {
    username: string;
    name: string;
    email: string;
    password: string;
    location: any;
};

type setFieldValueFunc = (field: string, value: any, shouldValidate?: boolean) => void;

type onChangeFunc = (value: OptionTypeBase | null, action: ActionMeta<OptionTypeBase>) => void;

const validationSchema = Yup.object({
    username: Yup.string().required().min(2).max(32),
    name: Yup.string().required().min(2).max(32),
    email: Yup.string().required().email().min(5).max(32),
    password: Yup.string().required().min(8).max(32)
});

export const SignUpForm = () => {

    const initialValues: FormValues = {username: '', name: '', email: '', password: '', location: ''};

    const isFormCompleted = (values: FormValues): boolean => {
        return values.username && values.name && values.email && values.password ? true: false;
    }

    const handleAutocompleteChange = (setFieldValue: setFieldValueFunc, fieldName: string): onChangeFunc => {

        const onChange = (value: OptionTypeBase | null, action: ActionMeta<OptionTypeBase>) => {
            console.log(value);
            console.log(action);
            setFieldValue(fieldName, value, false);
        };

        return onChange;
        
    };

    const handleSubmit = (values: FormValues, formikHelpers: FormikHelpers<FormValues>): void => {
        console.log(values);
        console.log(formikHelpers);
        const formValues = {
            ...values,
            location: values.location.label
        }
        formikHelpers.setSubmitting(false);
        // actions.resetForm();
    }

    
    return (
        <Formik
            initialValues={initialValues}
            validationSchema={validationSchema}
            onSubmit={handleSubmit}
        >
            {({values, setFieldValue, isSubmitting, isValid}) => (
                <StyledCard maxWidth='30rem'>
                    <StyledCardBody>
                        <StyledFormikForm>
                            
                            <TextInput placeholder='Username' name='username' type='text'/>
                            <InputError name='username' />
                               
                            <TextInput placeholder='Name' name='name' type='text'/>
                            <InputError name='name' />

                            <TextInput placeholder='Email' name='email' type='text'/>
                            <InputError name='email' />
      
                            <TextInput placeholder='Choose password' name='password' type='password'/>
                            <InputError name='password' />

                            <AutocompleteInput 
                                handleChange={handleAutocompleteChange(setFieldValue, 'location')}
                                types={GOOGLE_PLACES_API_TYPES}
                                fields={GOOGLE_PLACES_API_FIELDS}
                                name='location'
                                value={values.location}
                                validCountries={GOOGLE_PLACES_API_COUNTRIES}
                            />
                            
                            <PrimaryButton 
                                disabled={!isValid || !isFormCompleted(values) || isSubmitting} 
                                width='100%' 
                                padding='1.5rem' 
                                type='submit'
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

