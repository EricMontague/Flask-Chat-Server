import {StyledCard, StyledCardTitle, StyledCardBody, StyledCardFooter} from "./styles";


const Card = props => {
    return (
        <StyledCard>{props.children}</StyledCard>
    );
};


Card.Title = StyledCardTitle;
Card.Body = StyledCardBody;
Card.Footer = StyledCardFooter;


export default Card;