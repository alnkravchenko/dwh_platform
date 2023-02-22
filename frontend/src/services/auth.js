export default class Auth {
  loginUser = async (credentials) => {
    return fetch("http://localhost:8000/auth/login", {
      method: "POST",
      mode: "cors",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(credentials),
    }).then((data) => data.json());
  };

  signInUser = async (credentials) => {
    return fetch("http://localhost:8000/auth/sign_up", {
      method: "POST",
      mode: "cors",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(credentials),
    }).then((data) => data.json());
  };
}
