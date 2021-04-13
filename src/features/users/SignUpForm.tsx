import React from 'react';
import { Formik, FormikHelpers } from 'formik';
import * as Yup from 'yup';
import { OptionTypeBase, ActionMeta } from 'react-select';
import { StyledCard, StyledCardBody } from '../../common/components/cards/styles';
import { StyledFormikForm } from '../../common/components/forms/styles';
import { TextInput } from '../../common/components/formElements/TextInput';
import { InputError } from '../../common/components/formElements/InputError';
import AutocompleteInput from '../../common/components/formElements/AutocompleteInput';
import { PrimaryButton } from '../../common/components/buttons';
import { GOOGLE_PLACES_API_TYPES, GOOGLE_PLACES_API_FIELDS, GOOGLE_PLACES_API_COUNTRIES } from '../../constants';
import { register } from './usersSlice';
import { useAppDispatch } from '../../app/hooks';

type FormValues = {
    username: string;
    name: string;
    email: string;
    password: string;
    location: {label: string, value: any};
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

    const dispatch = useAppDispatch();

    const initialValues: FormValues = {
        username: '', 
        name: '', 
        email: '', 
        password: '', 
        location: {label: 'Jersey City, NJ, USA', value:{} }
    };

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
        const [city, state, country] = values.location.label.split(',');
        const formValues = {
            ...values,
            location: {city, state, country}
        }
        dispatch(register(formValues));
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

