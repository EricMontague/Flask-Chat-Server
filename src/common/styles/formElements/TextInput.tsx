import React from "react";
import PropTypes from 'prop-types';
import {useField} from 'formik';
import {StyledLabel, StyledInput, StyledInputContainer} from './styles';

type Props = {
    placeholder: string;
    name: string;
    disabled: boolean;
    label?: string;
    type: string;
};

export const TextInput = (props: Props) => {
    
    const [field, meta] = useField(props);
    if (props.label) {
        return (
            <>
                <StyledInputContainer>
                    <StyledLabel 
                        htmlFor={props.name}
                    >
                        {props.label}
                    </StyledLabel>
                    <StyledInput
                        {...field} 
                        placeholder={props.placeholder}
                        disabled={props.disabled}
                    />
                    
                </StyledInputContainer>
            </>  
        );
    }
    return (
        <>
            <StyledInputContainer>
                <StyledInput
                    {...field} 
                    type={props.type}
                    placeholder={props.placeholder}
                    disabled={props.disabled}
                />
            </StyledInputContainer>
        </>
    );
};

TextInput.defaultProps = {
    disabled: false
};

TextInput.propTypes = {
    placeholder: PropTypes.string.isRequired,
    name: PropTypes.string.isRequired,
    disabled: PropTypes.bool.isRequired,
    label: PropTypes.string,
    type: PropTypes.string.isRequired,
};


