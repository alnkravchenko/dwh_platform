import React from "react";
import { Button } from "react-bootstrap";
import { Link } from "react-router-dom";
import "../SignUpButton/SignUp.scss";

const SignUpButton = () => {
  return (
    <Link to="/sing_up" tabIndex="-1">
      <Button variant="outline-dark" className="signup-btn">
        SIGN UP
      </Button>
    </Link>
  );
};

export default SignUpButton;
