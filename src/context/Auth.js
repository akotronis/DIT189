import React, { createContext, useContext, useEffect, useState } from 'react';
// Create a new context for the access token
const AccessTokenContext = createContext();
export const useAccessToken = () => useContext(AccessTokenContext);

export const AccessTokenProvider = ({ children }) => {
  const [token, setToken] = useState('');

  useEffect(() => {
    // Check if the access token is already saved in local storage
    const storedAccessToken = localStorage.getItem('accessToken');
    const storedRefreshToken = localStorage.getItem('refreshToken');

    if (storedAccessToken && storedRefreshToken) {
      setToken({
        accessToken: storedAccessToken,
        refreshToken: storedRefreshToken,
      });
    }
  }, []);

  const saveToken = (token) => {
    // Save the access token to local storage
    localStorage.setItem('accessToken', token.accessToken);
    localStorage.setItem('refreshToken', token.refreshToken);

    // Update the access token in the context
    setToken(token);
  };

  const removeAccessToken = () => {
    // Remove the access token from local storage
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');

    // Clear the access token in the context
    setToken('');
  };

  return (
    <AccessTokenContext.Provider
      value={{ token, saveToken, removeAccessToken }}
    >
      {children}
    </AccessTokenContext.Provider>
  );
};
