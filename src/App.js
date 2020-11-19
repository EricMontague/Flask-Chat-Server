import GlobalStyles from "./globalStyles";
import UserProvider from "./providers";
import { ThemeProvider } from "styled-components";
import theme from "./theme";

const App = () => {
  return (
    <>
      <UserProvider>
        <ThemeProvider theme={theme}>
          <GlobalStyles />

          <h1>Hi There!</h1>

        </ThemeProvider>
      </UserProvider>
    </>
  );
}

export default App;


