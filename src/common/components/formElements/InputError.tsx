import React from 'react';
import PropTypes from 'prop-types';
import {StyledErrorMessage} from './styles';
import {ErrorMessage} from 'formik';
import {capitalizeString} from '../../utils';

type Props = {
    name: string;
};

export const InputError = (props: Props) => {
    return (
        <ErrorMessage name={props.name}>
            {message => (
                <StyledErrorMessage>
                    {capitalizeString(message)}
                </StyledErrorMessage>
            )}
        </ErrorMessage>
    )
};

InputError.propTypes = {
    name: PropTypes.string.isRequired
}