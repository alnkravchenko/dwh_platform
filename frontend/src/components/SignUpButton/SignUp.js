import React from "react";
import { Button } from "react-bootstrap";
import { Link } from "react-router-dom";
import "../SignUpButton/SignUp.scss";

const SignUpButton = ({ disabled }) => {
  const styles = disabled ? "disable-link" : "";

  return (
    <Link to="/sing_up" tabIndex="-1" className={styles}>
      <Button variant="outline-dark" className="signup-btn" disabled={disabled}>
        SIGN UP
      </Button>
    </Link>
  );
};

export default SignUpButton;
