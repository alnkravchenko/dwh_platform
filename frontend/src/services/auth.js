export default class AuthService {
  emailToUsername = email => email.split("@")[0];

  loginUser = async ({ email, password }) => {
    const username = this.emailToUsername(email);
    const credentials = { username, email, password };
    return fetch(`${process.env.REACT_APP_BACKEND_HOST}/auth/login`, {
      method: "POST",
      mode: "cors",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(credentials),
    }).then((data) => data.json());
  };

  signUpUser = async ({ email, password }) => {
    const username = this.emailToUsername(email);
    const credentials = { username, email, password };
    return fetch(`${process.env.REACT_APP_BACKEND_HOST}/auth/sign_up`, {
      method: "POST",
      mode: "cors",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(credentials),
    }).then((data) => data.json());
  };
}
