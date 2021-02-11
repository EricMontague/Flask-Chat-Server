import styled from "styled-components";
import { convertHexToRGBA, zIndex } from "src/components/globals";


export const MenuContainer = styled.nav`
    position: relative;
    display: flex;
    flex-direction: column;
    align-content: start;
    justify-content: stretch;
    left: 0;
    top: 0;
    bottom: 0;
    width: 18.75rem;
    color: ${props => props.theme.brand.alt};
    background-color: ${props => props.theme.bg.wash};
    padding-top: 3rem;
    box-shadow: ${Shadow.high} ${props => convertHexToRGBA(props.theme.bg.reverse, 0.25)}
    z-index: ${zIndex.fullscreen + 100};
`;


export const MobileMenu = styled.ul`
    display: flex;
    flex-direction: column;
    width: 100%;
    background: inherit;
`;



export const Fixed = style.div`
    display: ${props => (props.isOpen ? "flex" : "none")};
    top: 0;
    bottom: 0;
    left: 0;
    right: 0;
    width: 100vw;
    height: 100%;
    z-index: 1;
`;


export const MenuOverlay = styled.div`
    position: absolute;
    top: 0;
    bottom: 0;
    left: 0;
    right: 0;
    background-color: ${props => convertHexToRGBA(props.theme.bg.reverse, 0.5)};
`;