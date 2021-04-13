import styled from 'styled-components';
import { FlexCol } from '../globals';

type StyledCenteredLayoutProps = {
    marginTop?: string;
    marginBottom?: string;
};

export const StyledCenteredLayout = styled(FlexCol)<StyledCenteredLayoutProps>`
    padding: 1.5rem;
    margin-left: auto;
    margin-right: auto;
    margin-top: ${(props) => props.marginTop || '0'};
    margin-bottom: ${(props) => props.marginBottom || '0'};
`;
