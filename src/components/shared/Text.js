import { Box } from "@material-ui.core";


const Text = props => {
    return (
        <Box
            fontFamily={props.fontFamily}
            component="p"
            fontSize={16}
            color={props.color}
        />
    );
}

export default Text;