import React from 'react';
import {
    StyledLink,
    StyledButton,
    StyledPrimaryButton,
    StyledWarnButton,
    StyledOutlineButton,
    StyledHoverOutlineButton
} from './styles';
import {A} from '../globals';
import {StyledComponent} from 'styled-components';

export type ButtonProps = {
    href?: string;
    to?: string;
    target?: string;
    children: React.ReactNode;
    disabled?: boolean;
    isLoading?: boolean;
    padding?: string;
    width?: string;
    type: 'button' | 'submit' | 'reset';
};

const handleLinkWrapping = (ButtonComponent: StyledComponent<'button', any, ButtonProps, never>, props: ButtonProps) => {
    const {href, to, target, children, disabled, isLoading, ...rest} = props;

    const button = (
        <ButtonComponent disabled={disabled || isLoading} {...rest}>
            {children}
        </ButtonComponent>
    );
    
    // Return button wrapped in external link
    if (href !== undefined) {
        return (
            <A
                href={href}
                target={target || '_blank'}
                rel={!target ? 'nopener noreferrer': undefined}
            >
                {button}
            </A>
        );
    }

    // Return button wrapped in styled React Router Link
    if (to !== undefined) {
        return <StyledLink to={to}>{button}</StyledLink>;
    }

    // Return regular unwrapped button
    return button;
};


export const Button = (props: ButtonProps) => handleLinkWrapping(StyledButton, props);
export const PrimaryButton = (props: ButtonProps) => handleLinkWrapping(StyledPrimaryButton, props);
export const WarnButton = (props: ButtonProps) => handleLinkWrapping(StyledWarnButton, props);
export const OutlineButton = (props: ButtonProps) => handleLinkWrapping(StyledOutlineButton, props);
export const HoverOutlineButton = (props: ButtonProps) => handleLinkWrapping(StyledHoverOutlineButton, props);

