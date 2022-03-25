// import React, { useState, useEffect } from "react";
import Login from "./components/Login.js";
import Navbar from "./components/Navbar.js";
import Register from "./components/Register.js";

export default function App() {
  return (
    <div>
      <Navbar />
      <Login />
      <Register />
    </div>
  );
}
