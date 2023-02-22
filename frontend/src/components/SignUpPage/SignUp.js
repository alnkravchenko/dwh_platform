// import PropTypes from "prop-types";
import React, { useState } from "react";
import { Button } from "react-bootstrap";
import Auth from "../../services/auth";
import "../LoginPage/Login.scss";

const SignUp = () => {
  const [username, setUserName] = useState();
  const [password, setPassword] = useState();

  const handleSubmit = async (e) => {
    e.preventDefault();
    const token = await Auth().signInUser({
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
        <form
          onSubmit={handleSubmit}
          className="centered login-box"
          style={{ "padding-bottom": "69px" }}
        >
          <h1 className="header login-header">User Sign Up</h1>
          <input
            type="text"
            className="login-inpt"
            placeholder="Email address"
            onChange={(e) => setUserName(e.target.value)}
          />
          <input
            type="password"
            className="login-inpt"
            placeholder="Password"
            onChange={(e) => setPassword(e.target.value)}
          />
          <Button variant="dark" type="submit" className="login-btn">
            SIGN UP
          </Button>
        </form>
      </div>
    </>
  );
};

// Login.propTypes = {
//   setToken: PropTypes.func.isRequired,
// };

export default SignUp;
