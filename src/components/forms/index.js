import React from "react";
import {Input} from "../formElements";


export class SignUpForm extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            username: "",
            name: "",
            email: "",
            password: ""
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
            <form onSubmit={this.handleSubmit}>
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
                <Input
                    id="email"
                    type="text" 
                    placeholder="Email"
                    name="email"
                    value={this.state.email}
                    withLabel={false}
                    handleChange={this.handleChange}
                />
                <Input
                    id="password"
                    type="password" 
                    placeholder="Password"
                    name="password"
                    value={this.state.password}
                    withLabel={false}
                    handleChange={this.handleChange}
                />
                {/* <LocationField /> */}
                <PrimaryButton type="submit">Create account</PrimaryButton>
            </form>
        )
    }
    
};

