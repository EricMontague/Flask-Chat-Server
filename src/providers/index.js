import React, { useState, useEffect, useContext } from "react";
import PropTypes from "prop-types";


const UserContext = React.createContext(null);


export const useUserContext = () => {
    return useContext(UserContext);
};


const UserProvider = props => {
    const [currentUser, setCurrentUser] = useState(null);

    useEffect(() => {
        (async () => {
            const response = await fetch("src/data/user.json");
            if (!response.ok) {
                throw new Error("Failed with status code " + response.status)
            }
            const results = await response.json();
            setCurrentUser(results["@ericmont"]);

        })();
    }, [])


    return (
        <UserContext.Provider value={currentUser}>
            {props.children}
        </UserContext.Provider>
    )

};



UserProvider.propTypes = {
    children: PropTypes.element.isRequired
};

export default UserProvider;