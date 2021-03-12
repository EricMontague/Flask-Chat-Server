import PropTypes from 'prop-types';
import {useField, ErrorMessage} from 'formik';
import {StyledLabel, StyledInput, StyledInputContainer, StyledErrorMessage} from './styles';
import {capitalizeString} from '../../utils';


export const TextInput = props => {
    
    const [field, meta] = useField(props);
    if (props.label) {
        return (
            <>
                <StyledInputContainer>
                    <StyledLabel 
                        htmlFor={props.id || props.name}
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



export const InputError = props => {
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