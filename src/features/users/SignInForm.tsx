import React from 'react';
import { Formik, FormikHelpers } from 'formik';
import * as Yup from 'yup';
import { StyledCard, StyledCardBody } from '../../common/components/cards/styles';
import { StyledFormikForm } from '../../common/components/forms/styles';
import { TextInput } from '../../common/components/formElements/TextInput';
import { InputError } from '../../common/components/formElements/InputError';
import { PrimaryButton } from '../../common/components/buttons';
import { useAppDispatch } from '../../app/hooks';
import{ login } from './usersSlice';

type FormValues = {
    username: string;
    password: string;
};

const validationSchema = Yup.object({
    username: Yup.string().required().min(2).max(32),
    password: Yup.string().required().min(8).max(32)
})

export const SignInForm = () => {

    const dispatch = useAppDispatch();

    const initialValues: FormValues = {username: '', password: ''};

    const isFormCompleted = (values: FormValues): boolean => {
        return values.username && values.password ? true : false;
    };

    const handleSubmit = (values: FormValues, formikHelpers: FormikHelpers<FormValues>) => {
        console.log(values);
        console.log(formikHelpers);
        dispatch(login({...values}));
    };

    return (
        <Formik
            initialValues={initialValues}
            validationSchema={validationSchema}
            onSubmit={handleSubmit}
        >
            {({values, isValid, isSubmitting}) => (
                <StyledCard maxWidth='25rem'>
                    <StyledCardBody>
                        <StyledFormikForm>
                            <TextInput name='username' placeholder='Username' type='text'/>
                            <InputError name='username'/>

                            <TextInput name='password' placeholder='Password' type='password'/>
                            <InputError name='password'/>

                            <PrimaryButton 
                                disabled={!isValid || !isFormCompleted(values) || isSubmitting}
                                width='100%' 
                                padding='1rem' 
                                type='submit'
                            >
                                SignIn
                            </PrimaryButton>
                        </StyledFormikForm>
                    </StyledCardBody>
                </StyledCard>
            )}
        </Formik>
    );
};