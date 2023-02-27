import React from "react";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import Auth from "./components/AuthenticationPage/Auth";
import NotFound from "./components/Errors/NotFound";
import SignUpButton from "./components/SignUpButton/SignUp";
import AuthService from "./services/auth";

const authService = new AuthService();

const App = () => {
  return (
    <>
      <BrowserRouter>
        <Routes>
          <Route
            exact
            path="/"
            element={
              <Auth
                pageName="Login"
                authFunc={authService.loginUser}
                extraComponent={<SignUpButton />}
              />
            }
          />
          <Route
            path="/sing_up"
            element={
              <Auth pageName="Sign Up" authFunc={authService.signUpUser} />
            }
          />
          <Route path="*" element={<NotFound />} />
        </Routes>
      </BrowserRouter>
    </>
  );
};

export default App;
