import React from "react";
import PropTypes from "prop-types";
import {useField, ErrorMessage} from "formik";
import {StyledLabel, StyledInput, StyledInputContainer} from "./styles";


export const TextInput = props => {
    // useField() returns [formik.getFieldProps(), formik.getFieldMeta()]
    
    const [field, meta] = useField(props);
    if (meta.touched) {
        console.log(meta.error);
    }
    if (props.label) {
        return (
            <>
                <StyledLabel 
                    htmlFor={props.id || props.name}
                >
                    {props.label}
                </StyledLabel>
                <StyledInputContainer>
                    <StyledInput
                        {...field} 
                        placeholder={props.placeholder}
                        disabled={props.disabled}
                    />
                    <ErrorMessage name={field.name}/>
                </StyledInputContainer>
            </>
            
        );
    }
    return (
        <StyledInputContainer>
            <StyledInput
                {...field} 
                placeholder={props.placeholder}
                disabled={props.disabled}
            />
            <ErrorMessage name={field.name}/>
        </StyledInputContainer>
    );
};


TextInput.defaultProps = {
    disabled: false
};


TextInput.propTypes = {
    placeholder: PropTypes.string.isRequired,
    name: PropTypes.string.isRequired,
    disabled: PropTypes.bool.isRequired,
    label: PropTypes.string
};