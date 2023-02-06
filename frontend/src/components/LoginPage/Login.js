// import PropTypes from "prop-types";
import React, { useState } from "react";
import { Button } from "react-bootstrap";
import { Link } from "react-router-dom";
import loginUser from "../../controllers/login";
// import "../../styles/common.scss";
import "./Login.scss";

const Login = () => {
  const [username, setUserName] = useState();
  const [password, setPassword] = useState();

  const handleSubmit = async (e) => {
    e.preventDefault();
    const token = await loginUser({
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
        <Link to="/registration">
          <Button variant="outlined light">Registration</Button>
        </Link>
        <form onSubmit={handleSubmit} className="centered login-box">
          <h1 className="header login-label">User Login</h1>
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
        </form>
      </div>
    </>
  );
};

// Login.propTypes = {
//   setToken: PropTypes.func.isRequired,
// };

export default Login;
