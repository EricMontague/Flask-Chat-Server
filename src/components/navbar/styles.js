import styled from "styled-components";
import { convertHexToRGBA } from "../globals";


export const MenuContainer = styled.nav`
    position: relative;
    display: flex;
    flex-direction: column;
    align-content: start;
    justify-content: stretch;
    left: 0;
    top: 0;
    bottom: 0;
    width: 300px;
    background-color: ${props => props.theme.bg.wash};
    padding-top: ${props => props.hasNavBar ? "48px" : isDesktopApp() ? "40px" : "0"}
    box-shadow: ${Shadow.high} ${props => convertHexToRGBA(props.theme.bg.reverse, 0.25)}
`;


export const MobileMenu = styled.ul`
    display: flex;
    flex-direction: column;
    width: 100%;
    background: inherit;
`;


export const MobileMenuItem = styled.li`
    display: flex;
    align-items: center;
    justify-content: start;
`;


export const Fixed = style.div`
    display: ${props => (props.open ? "flex" : "none")};
    top: 0;
    bottom: 0;
    left: 0;
    right: 0;
    width: 100vw;
    height: 100%;
    z-index: 1;
`;