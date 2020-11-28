import React, { useState, useEffect, useContext } from "react";
import PropTypes from "prop-types";

const users = [
    {
        username: "@ericmont",
        name: "Eric Montague",
        email: "eric@gmail.com",
        communites: [],
        notifications: [],
        incomingInvites: [],
        outgoingInvites: [],
        imageUrl: "https://avatars0.githubusercontent.com/u/53024034?s=460&v=4"
    }
]

const UserContext = React.createContext(null);


export const useUserContext = () => {
    return useContext(UserContext);
};


const UserProvider = props => {
    const [currentUser, setCurrentUser] = useState(null);

    useEffect(() => {
        setCurrentUser(users[0]);
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