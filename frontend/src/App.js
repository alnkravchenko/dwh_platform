import React from "react";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import NotFound from "./components/Errors/NotFound";
import Login from "./components/LoginPage/Login";
import Registration from "./components/RegistrationPage/Registration";

const App = () => {
  return (
    <>
      <BrowserRouter>
        <Routes>
          <Route exact path="/" element={<Login />} />
          <Route path="/registration" element={<Registration />} />
          <Route path="*" element={<NotFound />} />
        </Routes>
      </BrowserRouter>
    </>
  );
};

export default App;
