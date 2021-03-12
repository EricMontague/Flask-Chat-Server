import PropTypes from "prop-types";
import {FlexRow} from "../globals";
import {StyledNavbarTransparent, StyledNavbarMenu, StyledNavbarMenuItem} from "./styles";
import {HoverOutlineButton} from "../buttons";
import {StyledHoverLink} from "../buttons/styles";
import {WhiteLogo} from "../logo";



export const TopNavbarTransparent = props => {
    return (
        <StyledNavbarTransparent>
            <FlexRow>
                <WhiteLogo />
                <StyledNavbarMenu justifyContent="flex-end">
                    <StyledNavbarMenuItem>
                        <StyledHoverLink to="/sign-in" color={props.linkColor}>
                            Sign In
                        </StyledHoverLink>
                    </StyledNavbarMenuItem>
                    <StyledNavbarMenuItem>
                        <HoverOutlineButton to="/sign-up">Sign Up</HoverOutlineButton>
                    </StyledNavbarMenuItem>
                </StyledNavbarMenu>
            </FlexRow>
        </StyledNavbarTransparent>
    );
};


TopNavbarTransparent.propTypes = {
    linkColor: PropTypes.string.isRequired
}