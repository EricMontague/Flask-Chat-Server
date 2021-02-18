import styled from "styled-components";
import zIndex from "../globals";


const NavbarBase = styled.nav`
    position: sticky;
    top: 0;
    left: 0;
    right: 0;
    height: 4rem;
    padding: 1rem 2rem;
    z-index: ${zIndex.navbar};
`;

export const NavbarLight = styled(NavbarBase)`
    color: ${props => props.theme.text.default};
    background-color: ${ props => props.theme.bg.light}
`;

export const NavbarTransparent = styled(NavbarBase)`
    color: inherit;
    background-color: transparent;
`;