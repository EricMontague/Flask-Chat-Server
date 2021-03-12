import PropTypes from 'prop-types';

import {Formik} from 'formik';

import * as Yup from 'yup';

import {StyledCard, StyledCardBody} from '../../../components/cards/styles';
import {StyledFormikForm} from '../../../components/forms/styles';
import {TextInput, InputError} from '../../../components/formElements';
import {PrimaryButton} from '../../../components/buttons';

const validationSchema = Yup.object({
    email: Yup.string().required().min(2).max(32),
    password: Yup.string().required().min(8).max(32)
})

export const SignInForm = props => {

    const isFormCompleted = values => {
        for (const field in values) {
            if (values[field] === '') {
                return false;
            }
        }
        return true
    };

    const handleSubmit = (values, actions) => {
        console.log(values);
        console.log(actions);
    };

    return (
        <Formik
            initialValues={{email: '', password: ''}}
            validationSchema={validationSchema}
            onSubmit={handleSubmit}
        >
            {({values, errors, isValid, isSubmitting}) => (
                <StyledCard maxWidth='25rem'>
                    <StyledCardBody>
                        <StyledFormikForm>
                            <TextInput name='email' placeholder='Email' type='text'/>
                            <InputError name='email'/>

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