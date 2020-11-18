import styled, { css } from "styled-components";
import theme from "../../theme";


export const convertHexToRGBA = (hex, alpha) => {
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


export const Shadow = {
    low: "0 2px 8px",
    mid: "0 4px 12px",
    high: "0 8px 16px"
};


export const Transition = {
    hover: {
        on: "all 0.2s ease-in",
        off: "all 0.2s ease-out"
    },
    reaction: {
        on: "all 0.15s ease-in",
        off: "all 0.1s ease-out"
    },
    dropdown: {
        off: "all 0.35s ease-out"
    }

}


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
    font-size: 0.875rem;
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
export class ZIndex {
    constructor() {
        this.base = 100; // Base Z-index level
        this.background = this.base - 1; // Content that should always be behind the base
    }

};

export const FlexRow = styled.div`
    display: flex;
    flex-direction: row;
    justify-content: flex-start;
    align-items: center;
`;

export const FlexCol = styled.div`
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    align-items: stretch;
`;