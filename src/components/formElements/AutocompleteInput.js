import PropTypes from 'prop-types';
import {StyledInputContainer} from './styles';
import GooglePlacesAutocomplete from 'react-google-places-autocomplete';
import theme from '../../theme';


// type AutocompleteProps = {
//   validCountries: string [];
//   handleAutocompleteChange: (value: any, actions: any) => void;
//   types: string [];
//   fields: string [];
//   name: string;
//   value: string;

// };


const autoCompleteStyles = {
  input: (provided) => ({
    ...provided,
    padding: '0.85rem 0.75rem'
  }),
  placeholder: (provided) => ({
    ...provided,
    paddingLeft: '0.75rem'
  }),
  container: (provided) => ({
    ...provided,
    width: '100%',
    fontSize: '1rem',
    color: theme.text.default
  }),
  control: (provided) => ({
    ...provided,
    borderColor: theme.input.border,
    boxShadow: 'none',
    '&:hover': {
      borderColor: '#e0e3e5'
    },
    '&:focus-within': {
      outline: 'none',
      borderColor: theme.bg.primary
    }
  }),
};



const AutocompleteInput = (props) => {
  return (
    <StyledInputContainer>
        <GooglePlacesAutocomplete
            apiKey={process.env.REACT_APP_GCP_API_KEY}
            selectProps={{
              styles: autoCompleteStyles,
              value: props.value,
              onChange: props.handleChange,
              placeholder: 'Choose location'
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
  handleChange: PropTypes.func.isRequired,
  types: PropTypes.arrayOf(PropTypes.string.isRequired),
  fields: PropTypes.arrayOf(PropTypes.string.isRequired),
  name: PropTypes.string.isRequired,
  value: PropTypes.object
};

export default AutocompleteInput;