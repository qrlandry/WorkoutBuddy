import './App.css';
import { UserContext } from "./UserContext.jsx";
import Home from "./Components/Home";
import Login from "./Components/Login.jsx";
import Register from "./Components/Register.jsx";
import Profile from './Components/Profile';
import { Routes, Route } from "react-router-dom";
import { useState, useContext, useEffect } from "react";
import { CheckSession } from "./Services/auth";
import Client from "./Services/api";
import { BASE_URL } from "./Services/api";

function App() {
  const [loggedIn, setLoggedIn] = useState(
    localStorage.getItem("loggedIn") === "true");
  const [user, setUser] = useState(null);

  const handleLogOut = () => {
    localStorage.removeItem("jwt");
    setLoggedIn(false);
    setUser(null);
  };

  useEffect(() => {
    const getSession = async () => {
      const sessionUser = await CheckSession();
      setUser(sessionUser);
      setLoggedIn(sessionUser !== null);
    };

    getSession();
  }, []);

  useEffect(() => {
    if (user !== null) {
      console.log("THE USER IS ", user);
    };
  }, [user]);;
  

  return (
    <div className="App">
      <UserContext.Provider
        value={{ loggedIn, setLoggedIn, user, setUser, handleLogOut }}
      >
        <main>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/profile" element={<Profile />} />
          </Routes>
        </main>
        </UserContext.Provider>
    </div>
  );
}

export default App;
