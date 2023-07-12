import { createContext, useContext, useState } from "react";
import { useLocation, Navigate, Outlet } from "react-router-dom";
import { useLocalStorage } from "../utils/useLocalStorage";
const AuthContext = createContext(null);

export const useAuth = () => useContext(AuthContext);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useLocalStorage("user", null);;

  return (
    <AuthContext.Provider value={{ user, setUser }}>
      {children}
    </AuthContext.Provider>
  );
};

export const RequireAuth = () => {
  const { user } = useAuth();
  const location = useLocation();

  if (!user) {
    return (
      <Navigate
        to={{ pathname: "/", state: { from: location } }}
        replace
      />
    );
  }

  return <Outlet />;
};