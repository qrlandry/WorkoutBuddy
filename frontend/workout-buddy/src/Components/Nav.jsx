import { NavLink } from "react-router-dom";
import { useNavigate } from "react-router-dom";
import { useContext, useState } from "react";
import { UserContext } from "../UserContext";
import { LogoutUser } from "../Services/auth";

export default function Nav() {
  const navigate = useNavigate();
  const [onSignInPage, setOnSignInPage] = useState(false);
  const { loggedIn, setLoggedIn } = useContext(UserContext);

  const handleSignout = async (e) => {
    e.preventDefault();
    await LogoutUser();
    setLoggedIn(false);
    console.log("logged out!");
    navigate("/");
  };

  return(
    <div className="nav-container">
      <div className="nav-links">
        <div className="top-right">
          {loggedIn ? (
            <div className="cart">
              <NavLink to="/cart" className="menu-item">
                Cart
              </NavLink>
            </div>
          ) : null}
          {loggedIn ? (
            <div className="profile" style={{ marginRight: "1vw" }}>
              <NavLink to="/profile" className="menu-item">
                Profile
              </NavLink>
            </div>
          ) : null}
          {!loggedIn ? (
            <div className="signin">
              <NavLink to="/signin" className="menu-item">
                Sign In
              </NavLink>
            </div>
          ) : (
            <div className="signout">
              <NavLink to="/" className="menu-item" onClick={handleSignout}>
                Sign Out
              </NavLink>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
