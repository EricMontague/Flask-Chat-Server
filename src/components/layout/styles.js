import styled from 'styled-components';
import {FlexCol} from '../globals';

export const CenteredLayout = styled(FlexCol)`
    padding: 1.5rem;
    margin-left: auto;
    margin-right: auto;
    margin-top: ${props => props.marginTop || '0'};
    margin-bottom: ${props => props.marginBottom || '0'};
`;