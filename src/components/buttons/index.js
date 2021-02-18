import React from "react";
import {
    A,
    StyledLink,
    StyledButton,
    StyledPrimaryButton,
    StyledWarnButton,
    StyledOutlineButton
} from "./style";


const handleLinkWrapping = (ButtonComponent, props) => {
    const {href, to, target, children, disabled, isLoading, ...rest} = props;
    
    const button = (
        <ButtonComponent disabled={disabled || isLoading } {...rest}>
            {children}
        </ButtonComponent>
    );
    
    
    // Return button wrapped in external link
    if (href) {
        return (
            <A
                href={href}
                target={target || "_blank"}
                rel={!target ? "nopener noreferrer": undefined}
            >
                {button}
            </A>
        )
    }

    // Return button wrapped in styled React Router Link
    if (to) {
        return <StyledLink to={to}>{button}</StyledLink>
    }

    // Return regular unwrapped button
    return button;
}


export const Button = props => handleLinkWrapping(StyledButton, props);
export const PrimaryButton = props => handleLinkWrapping(StyledPrimaryButton, props);
export const WarnButton = props => handleLinkWrapping(StyledWarnButton, props);
export const OutlineButton = props => handleLinkWrapping(StyledOutlineButton, props);
