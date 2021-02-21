import React from "react";
import PropTypes from "prop-types";
import {StyledLabel, StyledInput} from "./styles";


export const Input = props => {
    
    if (props.withLabel) {
        return (
            <>
                <StyledLabel {...props}>props.label</StyledLabel>
                <StyledInput 
                    id={props.id}
                    type={props.type}
                    placeholder={props.placeholder}
                    name={props.name}
                    value={props.value}
                    disabled={props.disabled}
                    onChange={props.handleChange}
                />
            </>
            
        );
    }
    return (
        <StyledInput 
            id={props.id}
            type={props.type}
            placeholder={props.placeholder}
            name={props.name}
            value={props.value}
            disabled={props.disabled}
            onChange={props.handleChange}
        />
    );
};


Input.defaultProps = {
    disabled: false
};


Input.propTypes = {
    id: PropTypes.string.isRequired,
    type: PropTypes.string.isRequired,
    placeholder: PropTypes.string.isRequired,
    name: PropTypes.string.isRequired,
    value: PropTypes.string.isRequired,
    disabled: PropTypes.bool.isRequired,
    withLabel: PropTypes.bool.isRequired,
    label: PropTypes.string,
    handleChange: PropTypes.func.isRequired
};