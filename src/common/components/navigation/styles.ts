import styled from 'styled-components';
import { zIndex, flexCenteredMixin, media } from '../globals';

type NavbarBaseProps = {
    position?: string;
};

type StyledNavbarMenuProps = {
    justifyContent?: string;
    flexGrow?: string;
    flexShrink?: string;
};

const NavbarBase = styled.nav<NavbarBaseProps>`
    position: ${(props) => props.position || 'static'};
    top: 0;
    left: 0;
    right: 0;
    height: 4rem;
    padding: 1rem 2rem;
    z-index: ${zIndex.navbar};
`;

export const StyledNavbarLight = styled(NavbarBase)`
    color: ${(props) => props.theme.text.default};
    background-color: ${(props) => props.theme.bg.light}
`;

export const StyledNavbarTransparent = styled(NavbarBase)`
    color: inherit;
    background-color: transparent;
`;

export const StyledNavbarMenu = styled.ul<StyledNavbarMenuProps>`
    display: flex;
    align-items: center;
    justify-content: ${(props) => props.justifyContent || 'flex-start'};
    flex-grow: ${(props) => props.flexGrow || '1'};
    flex-shrink: ${(props) => props.flexShrink || '0'};
    flex-basis: auto;

    ${media.small} {
        display: none;
    }
`;

export const StyledNavbarMenuItem = styled.li`
    ${flexCenteredMixin};
    margin-left: 1rem;
`;
