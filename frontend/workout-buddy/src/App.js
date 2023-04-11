import "./App.css";
import { UserContext } from "./UserContext.jsx";
import Home from "./Components/Home";
import Login from "./Components/Login.jsx";
import Register from "./Components/Register.jsx";
import Profile from "./Components/Profile";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { useState, useContext, useEffect } from "react";
import { CheckSession } from "./Services/auth";

function App() {
  const [loggedIn, setLoggedIn] = useState(
    localStorage.getItem("loggedIn") === "true"
  );
  const [user, setUser] = useState(null);

  return (
    <div className="App">
      <UserContext.Provider
        value={{ loggedIn, setLoggedIn, user, setUser }}
      >
        <main>
          <BrowserRouter>
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/login" element={<Login />} />
              <Route path="/register" element={<Register />} />
              <Route path="/profile" element={<Profile />} />
            </Routes>
          </BrowserRouter>
        </main>
      </UserContext.Provider>
    </div>
  );
}

export default App;
