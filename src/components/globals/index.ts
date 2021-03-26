import styled, { css } from 'styled-components';
import theme from '../../theme';

export const convertHexToRGBA = (hex: string, alpha: number) => {
    const r = parseInt(hex.slice(1, 3), 16);
    const g = parseInt(hex.slice(3, 5), 16);
    const b = parseInt(hex.slice(5, 7), 16);

    if (alpha >= 0) {
        return `rgba(${r}, ${g}, ${b}, ${alpha})`;
    }
    return `rgb(${r}, ${g}, ${b})`;
}

export const fontStack = css`
  font-family: -apple-system, BlinkMacSystemFont, 'Helvetica', 'Segoe',
    sans-serif;
`;

export const flexCenteredMixin = css`
    display: flex;
    justify-content: center;
    align-items: center;
`;

export const Shadow = {
    low: '0 2px 8px',
    mid: '0 4px 12px',
    high: '0 8px 16px'
};

export const Transition = {
    hover: {
        on: 'all 0.2s ease-in',
        off: 'all 0.2s ease-out'
    },
    reaction: {
        on: 'all 0.15s ease-in',
        off: 'all 0.1s ease-out'
    },
    dropdown: {
        off: 'all 0.35s ease-out'
    }

}

export const A = styled.a`
    display: flex;
    align-items: center;
    flex: none;
`;

export const H1 = styled.h1`
    ${fontStack};
    color: ${theme.text.default};
    font-weight: 900;
    font-size: 1.5rem;
    line-height: 1.3;
    margin: 0;
    padding: 0;
`;

export const H2 = styled.h2`
    ${fontStack};
    color: ${theme.text.default};
    font-weight: 700;
    font-size: 1.25rem;
    line-height: 1.3;
    margin: 0;
    padding: 0;
`;

export const H3 = styled.h3`
    ${fontStack};
    color: ${theme.text.default};
    font-weight: 500;
    font-size: 1rem;
    line-height: 1.5;
    margin: 0;
    padding: 0;
`;

export const H4 = styled.h4`
    ${fontStack};
    color: ${theme.text.default};
    font-weight: 500;
    font-size: 0.875rem;
    line-height: 1.4;
    margin: 0;
    padding: 0;
`;

export const H5 = styled.h5`
  ${fontStack};
  color: ${theme.text.default};
  font-weight: 500;
  font-size: 0.75rem;
  line-height: 1.4;
  margin: 0;
  padding: 0;
`;

export const H6 = styled.h6`
  ${fontStack};
  color: ${theme.text.default};
  font-weight: 600;
  text-transform: uppercase;
  font-size: 0.675rem;
  line-height: 1.5;
  margin: 0;
  padding: 0;
`;

export const P = styled.p`
    ${fontStack};
    color: ${theme.text.default};
    font-weight: 400;
    font-size: 1rem;
    line-height: 1.4;
    margin: 0;
    padding: 0;
`;

export const Span = styled.span`
    ${fontStack};
    color: ${theme.text.default};
    font-weight: 400;
    font-size: 0.875rem;
    line-height: 1.4;
    margin: 0;
    padding: 0;
`;

// Defines a Z-index hierarchy between all elements in the app
class ZIndex {

    readonly base: number;
    readonly background: number;
    readonly hidden: number;
    readonly card: number;
    readonly loading: number;
    readonly avatar: number;
    readonly formElement: number;
    readonly navbar: number;
    readonly dropDowns: number;
    readonly fullScreen: number;
    readonly modal: number;
    readonly tooltip: number;

    constructor() {
        this.base = 100; // Base Z-index level
        this.background = this.base - 100; // Content that should always be behind the base
        this.hidden = this.base - 200; // Content that should be hidden completely

        this.card = this.base + 100; // Cards should default to one layer above base content
        this.loading = this.card + 100; // Loading should appear above cards
        this.avatar = this.card + 100; // Avatars should appear above cards
        this.formElement = this.card + 100; // Form elements should appear above cards

        this.navbar = 3000;
        this.dropDowns = this.navbar + 100; // dropdowns shouldn't appear below the navbar
        this.fullScreen = 4000; // For fullscreen elements should cover all content except for modals and tooltips
        this.modal = 5000; // modals should show about fullscreen elements
        this.tooltip = 6000; // tooltips should always be on top of every element
    }

};

export const zIndex = new ZIndex();

const SMALL_BREAKPOINT = 576;
const MEDIUM_BREAKPOINT = 768;
const LARGE_BREAKPOINT = 992;
const EXTRA_LARGE_BREAKPOINT = 1200;
const EXTRA_EXTRA_LARGE_BREAKPOINT = 1400;

const customMediaQuery = (maxWidth: number) => {
    return `@media (max-width: ${maxWidth}px)`;
};

export const media = {
custom: customMediaQuery,
    small: customMediaQuery(SMALL_BREAKPOINT),
    medium: customMediaQuery(MEDIUM_BREAKPOINT),
    large: customMediaQuery(LARGE_BREAKPOINT),
    extra_large: customMediaQuery(EXTRA_LARGE_BREAKPOINT),
    extra_extra_large: customMediaQuery(EXTRA_EXTRA_LARGE_BREAKPOINT)
}

type FlexProps = {
    justifyContent?: string;
    alignItems?: string;
};

type GridProps = {
    cols: string;
    gap: string;
};

export const FlexRow = styled.div<FlexProps>`
    display: flex;
    flex-direction: row;
    justify-content: ${props => props.justifyContent || 'flex-start'};
    align-items: ${props => props.alignItems || 'center'};
`;

export const FlexCol = styled.div<FlexProps>`
    display: flex;
    flex-direction: column;
    flex: 1;
    justify-content: ${props => props.justifyContent || 'flex-start'};
    align-items: ${props => props.alignItems || 'stretch'};
`;

export const GridCol = styled.div<GridProps>`
    display: grid;
    grid-template-column: repeat(${props => props.cols});
    gap: ${props => props.gap};
`;