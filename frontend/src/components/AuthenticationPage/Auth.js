import PropTypes from "prop-types";
import React, { useState } from "react";
import { Alert, Button } from "react-bootstrap";
import DocumentTitle from "react-document-title";
import { useAuthService } from "../../services/auth";
import "./Auth.scss";

const Auth = ({ pageName, authFunc, extraComponent }) => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [authLoading, setAuthLoading] = useState(false);

  const authService = useAuthService();
  const { error, clearError } = authService;
  const auth = authService[authFunc];

  const handleSubmit = async (e) => {
    e.preventDefault();
    setAuthLoading(true);
    clearError();
    await new Promise((r) => setTimeout(r, 1000));
    const response = await auth({
      email,
      password,
    });
    console.log(response);
    setAuthLoading(false);
  };

  const errorMessage = error ? <Alert variant="danger">{error}</Alert> : null;

  return (
    <DocumentTitle title={pageName}>
      <>
        <div className="split left">
          <img
            className="background-image"
            src={`${process.env.PUBLIC_URL}/images/auth_background.png`}
            alt="Background"
          />
        </div>
        <div className="split right">
          <form onSubmit={handleSubmit} className="centered auth-box">
            <h1 className="header auth-header">User {pageName}</h1>
            <input
              type="text"
              className="auth-inpt"
              placeholder="Email address"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
            <input
              type="password"
              className="auth-inpt"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
            <Button
              variant="dark"
              type="submit"
              className="auth-btn"
              disabled={authLoading}
            >
              {pageName.toUpperCase()}
            </Button>
            {errorMessage}
            {extraComponent}
          </form>
        </div>
      </>
    </DocumentTitle>
  );
};

Auth.propTypes = {
  pageName: PropTypes.string.isRequired,
  authFunc: PropTypes.string.isRequired,
  extraComponent: PropTypes.element,
};

export default Auth;
