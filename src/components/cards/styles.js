import styled from "styled-components";
import {FlexCol, FlexRow, H3, zIndex} from "../globals";


export const StyledCard = styled(FlexCol)`
    padding: 1rem 0.75rem;
    background: ${props => props.theme.bg.default};
    border: 1px solid #eceff1;
    box-shadow: rgb(17 51 83 / 2%) 0px 4px 12px 0px;
    z-index: ${zIndex.card}
`;


export const StyledCardTitle = styled(H3)`
    text-align: center;
    padding-bottom: 1rem;
`;


export const StyledCardBody = styled(FlexCol)`
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    padding-bottom: 1rem;
`;


export const StyledCardFooter = styled(FlexRow)`
    justify-content: ${props => props.justifyStart ? "flex-start" : "flex-end"}
    padding-top: 0.5rem;
    padding-bottom: 0.5rem;
`;