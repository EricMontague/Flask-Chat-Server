import React, { useState } from "react";
import { Route } from "react-router-dom"
import { useUserContext } from "src/providers";
import PropTypes from "prop-types";



const Navigation = props => {
    const [isOpen, toggleNavigation] = useState(false);
    const currentUser = useUserContext();

    return (
        <NavigationWrapper isOpen={isOpen}>
            <Overlay
                show={isOpen}
                onClick={toggleNavigation}
            />
            <NavigationGrid isOpen={isOpen}>
                <Route path="/new/room"></Route>
                <Route path="/profile"></Route>
                <Route path="/explore"></Route>
                <Route path="/inbox"></Route>
                <Route path="/notifications"></Route>
                <Divider />
                <CommunityList />
                <Divider />
                <Route path="/new/community"></Route>
            </NavigationGrid>
        </NavigationWrapper>
    );

};

export default Navigation;