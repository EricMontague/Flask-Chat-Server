import 'styled-components';

declare module 'styled-components' {
    export interface DefaultTheme {
        bg: {
            default: string;
            primary: string;
            light: string;
            warn: string;
          },
          font: {
            default: string;
          },
          text: {
            default: string;
            primary: string;
            placeholder: string;
            white: string;
            warn: string;
          },
          input: {
            border: string;
            borderHover: string;
            placeholder: string;
          },
    }
};
