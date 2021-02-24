import React from "react";
import {StyledCard, StyledCardBody} from "../cards/styles";
import {StyledForm} from "./styles";
import {Input} from "../formElements";
import {StyledInputRow} from "../formElements/styles";
import {PrimaryButton} from "../buttons";


export class SignUpForm extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            username: "",
            name: "",
            email: "",
            password: "",
            isFormCompleted: false
        };
        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    handleChange(event) {
        this.setState({[event.target.name]: event.target.value});
    }

    handleSubmit(event) {
        event.preventDefault();
        alert("Login form submitted!");
    }

    render() {
        return (
            <StyledCard maxWidth="30rem">
                <StyledCardBody>
                    <StyledForm onSubmit={this.handleSubmit}>
                        <StyledInputRow>
                            <Input
                                id="username" 
                                type="text" 
                                placeholder="Username"
                                name="username"
                                value={this.state.username}
                                withLabel={false}
                                handleChange={this.handleChange}
                            />
                            <Input
                                id="name"
                                type="text" 
                                placeholder="Name"
                                name="name"
                                value={this.state.name}
                                withLabel={false}
                                handleChange={this.handleChange}
                            />
                        </StyledInputRow>
                        <StyledInputRow>
                            <Input
                                id="email"
                                type="text" 
                                placeholder="Email"
                                name="email"
                                value={this.state.email}
                                withLabel={false}
                                handleChange={this.handleChange}
                            />
                        </StyledInputRow>
                        <StyledInputRow>
                            <Input
                                id="password"
                                type="password" 
                                placeholder="Choose password"
                                name="password"
                                value={this.state.password}
                                withLabel={false}
                                handleChange={this.handleChange}
                            />
                        </StyledInputRow>
                        {/* <LocationField /> */}
                        <PrimaryButton disabled={!this.state.isFormCompleted} width="100%" padding="1.5rem" type="submit">
                            Create account
                        </PrimaryButton>
                    </StyledForm>
                </StyledCardBody>
            </StyledCard>
        )
    }
    
};

