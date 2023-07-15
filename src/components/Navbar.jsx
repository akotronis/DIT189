import { Box, Button, HStack, Heading, Spacer } from '@chakra-ui/react';
import keycloakCredentials from '../keycloak/getKeycloakCredentials';
import { useAccessToken } from '../context/Auth';
import { KEYCLOAK_LOGOUT_URL } from '../config/urls';

export default function Navbar() {
  const { token, removeAccessToken } = useAccessToken();
  const refreshToken = token.refreshToken;
  const headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
  };

  const handleLogout = async () => {
    try {
      const response = await fetch(KEYCLOAK_LOGOUT_URL, {
        method: 'POST',
        headers: headers,
        body: new URLSearchParams({
          client_id: keycloakCredentials.clientId,
          client_secret: keycloakCredentials.clientSecret,
          refresh_token: refreshToken,
        }),
      });

      if (response.ok) {
        // Logout was successful, perform any necessary cleanup or redirection
        console.log('Logout successful');
        removeAccessToken();
      } else {
        // Handle logout failure
        console.error('Logout failed');
      }
    } catch (error) {
      console.error('Error occurred during logout:', error);
    }
  };

  return (
    <Box px="20px" py="10px">
      <HStack spacing="20px">
        <Heading as="h1" fontSize="xl" color="white">
          e-Divorce
        </Heading>
        <Spacer />
        <Button
          onClick={handleLogout}
          colorScheme="whiteAlpha"
          variant="solid"
          color="blue.400"
          bg="white"
          _hover={{ bg: 'blue.200' }}
        >
          Logout
        </Button>
      </HStack>
    </Box>
  );
}
