import SearchTags from "./components/searchTags";
import ResetStyle from "./resetStyles";
import ThemeProvider from "styled-components";
import { StylesProvider } from "@material-ui/core/styles";
import theme from "./theme";

const App = () => {
  return (
    <>
      <StylesProvider injectFirst>
        <ThemeProvider theme={theme}>
          <ResetStyle />
          {/* <SearchTags
        searchEndPoint="https://api.bytehub.dev/api/v1/tags/search.json?q="
        onSelect={() => { }}
      /> */}
          <h1>Hi There!</h1>
        </ThemeProvider>
      </StylesProvider>
    </>
  );
}

export default App;


