// import PropTypes from "prop-types";
import React, { useState } from "react";
import { Button } from "react-bootstrap";
import { Link } from "react-router-dom";
import Auth from "../../services/auth";
import "./Login.scss";

const Login = () => {
  const [username, setUserName] = useState();
  const [password, setPassword] = useState();

  const handleSubmit = async (e) => {
    e.preventDefault();
    const token = await Auth().loginUser({
      username,
      password,
    });
    console.log(token);
  };

  return (
    <>
      <div className="split left">
        <img
          className="background-image"
          src={`${process.env.PUBLIC_URL}/images/login_background.png`}
          alt="Background"
        />
      </div>
      <div className="split right">
        <form onSubmit={handleSubmit} className="centered login-box">
          <h1 className="header login-header">User Login</h1>
          <label>
            <input
              type="text"
              className="login-inpt"
              placeholder="Email address"
              onChange={(e) => setUserName(e.target.value)}
            />
          </label>
          <label>
            <input
              type="password"
              className="login-inpt"
              placeholder="Password"
              onChange={(e) => setPassword(e.target.value)}
            />
          </label>
          <div>
            <Button variant="dark" type="submit" className="login-btn">
              LOGIN
            </Button>
          </div>
          <Link to="/sing_up">
            <Button variant="outline-dark" className="signup-btn">
              SIGN UP
            </Button>
          </Link>
        </form>
      </div>
    </>
  );
};

// Login.propTypes = {
//   setToken: PropTypes.func.isRequired,
// };

export default Login;
