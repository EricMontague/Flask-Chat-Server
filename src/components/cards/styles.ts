import styled from 'styled-components';
import { FlexCol, FlexRow, H3, zIndex } from '../globals';

type StyledCardProps = {
    width?: string;
    maxWidth?: string;
};

type StyledCardFooterProps = {
    justifyContent?: string;
};

export const StyledCard = styled(FlexCol)<StyledCardProps>`
    padding: 1.5rem;
    background: ${(props) => props.theme.bg.default};
    border: 1px solid #eceff1;
    border-radius: 0.25rem;
    box-shadow: rgb(17 51 83 / 2%) 0px 4px 12px 0px;
    z-index: ${zIndex.card};
    width: ${(props) => props.width || '100%'};
    max-width: ${(props) => props.maxWidth || '100%'};
`;

export const StyledCardTitle = styled(H3)`
    text-align: center;
    padding-bottom: 1rem;
`;

export const StyledCardBody = styled(FlexCol)`
    padding-bottom: 1rem;
`;

export const StyledCardFooter = styled(FlexRow)<StyledCardFooterProps>`
    justify-content: ${(props) => props.justifyContent || 'flex-end'}
    align-items: center;
    padding-top: 0.5rem;
    padding-bottom: 0.5rem;
`;
