import React, { useState } from "react";
import { MenuContainer, MenuOverlay, Fixed } from "./style";
import { Menu } from "react-feather";



const Menu = props => {
    const [isOpen, setIsOpen] = useState(false);

    const toggleMenu = () => {
        setIsOpen(!isOpen);
    };

    return (
        <>
            <Menu onClick={toggleMenu} />
            <Fixed isOpen={isOpen}>
                <MenuContainer>
                    {isOpen && props.children}
                </MenuContainer>
                <MenuOverlay onClick={toggleMenu} />
            </Fixed>
        </>
    );
};


export default Menu;