import React from 'react';
import PropTypes from 'prop-types';
import { StylesConfig, OptionTypeBase, ActionMeta } from 'react-select';
import GooglePlacesAutocomplete from 'react-google-places-autocomplete';
import { AutocompletionRequest, ApiOptions } from 'react-google-places-autocomplete/build/GooglePlacesAutocomplete.types';
import { StyledInputContainer } from './styles';
import theme from '../../theme';

type Props = {
  validCountries: string[];
  handleChange: (value: OptionTypeBase | null, action: ActionMeta<OptionTypeBase>) => void;
  types: string[];
  fields: string[];
  name: string;
  value: any;
};

type isMulti = false;

const autoCompleteStyles: StylesConfig<OptionTypeBase, isMulti> = {
  input: (provided) => ({
    ...provided,
    padding: '0.85rem 0.75rem',
  }),
  placeholder: (provided) => ({
    ...provided,
    paddingLeft: '0.75rem',
  }),
  container: (provided) => ({
    ...provided,
    width: '100%',
    fontSize: '1rem',
    color: theme.text.default,
  }),
  control: (provided) => ({
    ...provided,
    borderColor: theme.input.border,
    boxShadow: 'none',
    '&:hover': {
      borderColor: '#e0e3e5',
    },
    '&:focus-within': {
      outline: 'none',
      borderColor: theme.bg.primary,
    },
  }),
};

const AutocompleteInput = (props: Props) => {
  const {
    value, handleChange, fields, types, validCountries, name,
  } = props;
  const autocompletionRequest = { types, country: validCountries } as AutocompletionRequest;
  const apiOptions = { fields } as ApiOptions;

  return (
    <StyledInputContainer>
      <GooglePlacesAutocomplete
        apiKey={process.env.REACT_APP_GCP_API_KEY}
        selectProps={{
          value,
          name,
          inputId: name,
          styles: autoCompleteStyles,
          onChange: handleChange,
          placeholder: 'Choose location',
        }}
        apiOptions={apiOptions}
        autocompletionRequest={autocompletionRequest}
      />
    </StyledInputContainer>
  );
};

AutocompleteInput.propTypes = {
  validCountries: PropTypes.arrayOf(PropTypes.string.isRequired).isRequired,
  handleChange: PropTypes.func.isRequired,
  types: PropTypes.arrayOf(PropTypes.string.isRequired).isRequired,
  fields: PropTypes.arrayOf(PropTypes.string.isRequired).isRequired,
  name: PropTypes.string.isRequired,
  value: PropTypes.object.isRequired,
};

export default AutocompleteInput;
