import { useState, useCallback } from "react";
import { useNavigate } from "react-router-dom";

import { useAuth } from "../context/Auth";

const Login = () => {
  const [username, setUsername] = useState("");
  const { setUser } = useAuth();
  const navigate = useNavigate();

  const login = useCallback(
    (e) => {
      e.preventDefault();
      setUser({ username });
      navigate("/dashboard");
    },
    [setUser, username, navigate]
  );

  return (
    <div>
      <h1>Login page</h1>
      <p>This route has public access.</p>
      <form onSubmit={login}>
        <input
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          placeholder="Type username..."
        />
        <button type="submit">Login</button>
      </form>
    </div>
  );
};

export default Login;