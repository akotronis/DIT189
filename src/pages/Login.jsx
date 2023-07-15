import React, { useEffect } from 'react';
import { useAccessToken } from '../context/Auth';
import { keycloakCredentials } from '../config/config';
import RootLayout from '../layouts/RootLayout';
import { Box, Heading, Text, Button } from '@chakra-ui/react';

// Create a new context to store the access token globally

const Login = () => {
  const { token, saveToken } = useAccessToken();

  const handleLogin = () => {
    // Redirect the user to the authentication URL

    window.location.href = `${keycloakCredentials.kcUrl}/realms/${keycloakCredentials.realm}/protocol/openid-connect/auth?client_id=${keycloakCredentials.clientId}&response_type=code&state=fj8o3n7wgy1op5`;
  };

  useEffect(() => {
    const urlParams = new URLSearchParams(window.location.search);
    const authorizationCode = urlParams.get('code');
    const newUrl = new URL(window.location);
    newUrl.searchParams.delete('code');
    newUrl.searchParams.delete('state');
    newUrl.searchParams.delete('session_state');
    console.log(process.env.REACT_APP_BACKEND_API_URL);
    window.history.pushState({}, '', newUrl);
    if (authorizationCode && !token.accessToken) {
      // Exchange the authorization code for an access token
      fetch(
        `${keycloakCredentials.kcUrl}/realms/${keycloakCredentials.realm}/protocol/openid-connect/token`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
          },
          body: `client_id=${keycloakCredentials.clientId}&client_secret=${keycloakCredentials.clientSecret}&grant_type=authorization_code&code=${authorizationCode}`,
        }
      )
        .then((response) => response.json())
        .then((data) => {
          // Store the access token
          console.log(data.refresh_token);
          saveToken({
            accessToken: data.access_token,
            refreshToken: data.refresh_token,
          });
        })
        .catch((error) => {
          console.error(
            'Failed to exchange authorization code for access token:',
            error
          );
        });
    }
  }, [token.accessToken, saveToken]);

  if (token.accessToken) {
    return <RootLayout />;
  }

  return (
    <Box
      height="100vh"
      display="flex"
      alignItems="center"
      color={'white'}
      justifyContent="center"
      bgGradient="linear(to-r, blue.400, teal.400)"
    >
      <Box textAlign="center" p="8">
        <Heading as="h1" size="2xl" mb="4">
          eDivorce
        </Heading>
        <Text fontSize="lg" mb="8">
          It's time.
        </Text>
        <Button colorScheme="blue" onClick={handleLogin}>
          Login
        </Button>
      </Box>
    </Box>
  );
};

export default Login;
