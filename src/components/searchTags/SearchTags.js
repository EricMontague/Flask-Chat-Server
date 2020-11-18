import React, { useState, useEffect } from "react";
import TextField from "@material-ui/core/TextField";
import Autocomplete from "@material-ui/lab/Autocomplete";
import CircularProgress from "@material-ui/core/CircularProgress";
import SearchIcon from "@material-ui/icons/Search";
import { makeStyles } from "@material-ui/core/styles";
import { Tag, TagBox, OuterBox, SearchIconBox } from "./styles";
import PropTypes from "prop-types";

function SearchTags({ onSelect, searchEndPoint }) {
    const [open, setOpen] = useState(false);
    const [searchValue, setSearchValue] = useState("");
    const [options, setOptions] = useState([]);
    const [searchedTags, setSearchedTags] = useState([]);
    const loading = open && options.length === 0;

    useEffect(() => {
        setSearchedTags(getOldSearchValues());
    }, []);

    useEffect(() => {
        let active = true;
        (async () => {
            const response = await fetch(searchEndPoint + searchValue);
            const result = await response.json();
            if (active) {
                setOptions(result.tags);
                console.log(result.tags);
                if (searchedTags.length === 0 && getOldSearchValues().length === 0) {
                    setSearchedTags(result.tags.slice(0, 4));
                }
            }
        })();

        return () => {
            active = false;
        };
    }, [loading, searchValue]);

    useEffect(() => {
        if (!open) setOptions([]);
    }, [open]);

    const useStyles = makeStyles((theme) => ({
        root: {
            backgroundColor: "#f1f5f8",
            border: 0,
            "& .MuiOutlinedInput-root": {
                borderRadius: 10,
                fontWeight: 600,
                paddingLeft: "65px !important",
                "& fieldset": {
                    borderColor: "transparent",
                },
                "&:hover fieldset": {
                    borderColor: "transparent",
                },
                "&.Mui-focused fieldset": {
                    borderColor: "transparent",
                },
            },
        },
    }));

    const getOldSearchValues = () => {
        const storeData = localStorage.getItem("bythb:searchedValues");
        if (storeData) {
            return JSON.parse(storeData);
        }
        return [];
    };

    const appendSearchValues = (item) => {
        let values = getOldSearchValues();
        values.push(item);

        localStorage.setItem(
            "bythb:searchedValues",
            JSON.stringify(values.slice(0, 5))
        );
    };

    const classes = useStyles();
    return (
        <OuterBox>
            <Autocomplete
                id="asynchronous-demo"
                style={{ width: 400, borderRadius: 10, overflow: "hidden" }}
                open={open}
                onOpen={() => setOpen(true)}
                onClose={() => setOpen(false)}
                getOptionSelected={(option, value) => option.name === value.name}
                getOptionLabel={(option) => option.name}
                options={options}
                loading={loading}
                onChange={(event, newInputValue) => {
                    appendSearchValues(newInputValue);
                }}
                onInputChange={(event, newInputValue) => {
                    setSearchValue(newInputValue);
                    if (onSelect) onSelect(newInputValue);
                }}
                inputValue={searchValue}
                renderInput={(params) => (
                    <TextField
                        className={classes.root}
                        {...params}
                        value={searchValue}
                        placeholder="Search for components"
                        variant="outlined"
                        InputProps={{
                            ...params.InputProps,
                            startAdornment: (
                                <SearchIconBox>
                                    <SearchIcon />
                                </SearchIconBox>
                            ),
                            endAdornment: (
                                <React.Fragment>
                                    {loading ? (
                                        <CircularProgress color="inherit" size={20} />
                                    ) : null}
                                    {params.InputProps.endAdornment}
                                </React.Fragment>
                            ),
                        }}
                    />
                )}
            />
            <TagBox>
                {searchedTags.filter(Boolean).map(
                    (item) =>
                        item && (
                            <Tag
                                onClick={() => {
                                    setSearchValue(item.name);
                                    if (onSelect) onSelect(item.name);
                                }}
                                key={item.id}
                            >
                                {item.name}
                            </Tag>
                        )
                )}
            </TagBox>
        </OuterBox>
    );
}




SearchTags.propTypes = {
    onSelect: PropTypes.func,
    searchEndPoint: PropTypes.string,
};

export default SearchTags;