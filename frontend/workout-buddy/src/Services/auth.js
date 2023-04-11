import Client from "./api"
import axios from "axios";
const token = localStorage.getItem('jwt');
console.log('Token:', token);

if (token) {
  axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
}

export const setAuthToken = (token) => {
  if (token) {
    axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
  } else {
    delete axios.defaults.headers.common['Authorization'];
  }
};

export const RegisterUser = async (data) => {
  try {
    const res = await Client.post("/register", data);
    return res.data;
  } catch (error) {
    throw error;
  }
};

export const SignInUser = async (data, setUser) => {
  try {
    const res = await Client.post("/login", data);
    const token = res.data.jwt;
    setUser(res.data.user);
    setAuthToken(token); 
    localStorage.setItem('jwt', token); 
    return res.data;
  } catch (error) {
    console.error(error);
    throw error.res.data;
  }
};

export const CheckSession = async () => {
  try {
    if (localStorage.getItem("jwt")) {
      const response = await axios.get(
        "http://127.0.0.1:8000/api/user",
        {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("jwt")}`,
          },
        }
      );
      return response.data;
    }
    return null;
  } catch (error) {
    console.log(error);
    return null;
  }
};

export const LogoutUser = async () => {
  try {
    const res = await Client.post("/logout");
    localStorage.removeItem('jwt');
    return res.data;
  } catch (error) {
    throw error;
  }
};