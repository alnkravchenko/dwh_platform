import { useHttp } from "../hooks/http.hook";

export const useAuthService = () => {
  const { loading, request, error, clearError } = useHttp();

  // const _emailToUsername = (email) => email.split("@")[0];
  const _host = process.env.REACT_APP_BACKEND_HOST;

  const loginUser = async (credentials) => {
    const url = `${_host}/auth/login`;
    const res = await request(url, "POST", JSON.stringify(credentials));
    return res.details;
  };

  const signUpUser = async (credentials) => {
    const url = `${_host}/auth/sign_up`;
    const res = await request(url, "POST", JSON.stringify(credentials));
    return res.details;
  };

  return { loading, error, clearError, loginUser, signUpUser };
};
