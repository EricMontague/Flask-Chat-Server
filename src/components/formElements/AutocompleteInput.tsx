import React from "react";
import PropTypes from "prop-types";
import {StyledInputContainer} from "./styles";
import GooglePlacesAutocomplete from "react-google-places-autocomplete";


type AutocompleteProps = {
  validCountries: string [];
  handleAutocompleteChange: (value: any, actions: any) => void;
  types: string [];
  fields: string [];
  name: string;
  value: string;

};


const AutocompleteInput = (props: AutocompleteProps) => {

  return (
    <StyledInputContainer>
        <GooglePlacesAutocomplete
            apiKey={process.env.REACT_APP_GCP_API_KEY}
            selectProps={{
                value: props.value,
                onChange: props.handleAutocompleteChange
            }}
            apiOptions={{fields: props.fields}}
            autocompletionRequest={{types: props.types, country: props.validCountries}}
            name={props.name}
            id={props.name}
        />
      </StyledInputContainer>
  );
};

AutocompleteInput.propTypes = {
  validCountries: PropTypes.arrayOf(PropTypes.string.isRequired).isRequired,
  handleAutocompleteChange: PropTypes.func.isRequired,
  types: PropTypes.arrayOf(PropTypes.string.isRequired),
  fields: PropTypes.arrayOf(PropTypes.string.isRequired),
  name: PropTypes.string.isRequired,
  value: PropTypes.string.isRequired
};

export default AutocompleteInput;