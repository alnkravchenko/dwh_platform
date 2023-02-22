import React from "react";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import NotFound from "./components/Errors/NotFound";
import Login from "./components/LoginPage/Login";
import SignUp from "./components/SignUpPage/SignUp";

const App = () => {
  return (
    <>
      <BrowserRouter>
        <Routes>
          <Route exact path="/" element={<Login />} />
          <Route path="/sing_up" element={<SignUp />} />
          <Route path="*" element={<NotFound />} />
        </Routes>
      </BrowserRouter>
    </>
  );
};

export default App;
