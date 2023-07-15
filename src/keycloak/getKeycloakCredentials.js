import { KEYCLOAK_URL } from '../config/config';
function generateRandomString(length) {
  const characters = 'abcdefghijklmnopqrstuvwxyz0123456789';
  let randomString = '';

  for (let i = 0; i < length; i++) {
    const randomIndex = Math.floor(Math.random() * characters.length);
    randomString += characters.charAt(randomIndex);
  }

  return randomString;
}

const keycloakCredentials = {
  kcUrl: KEYCLOAK_URL,
  realm: process.env.REACT_APP_KEYCLOAK_REALM,
  clientId: process.env.REACT_APP_KEYCLOAK_CLIENT_ID,
  clientSecret: process.env.REACT_APP_KEYCLOAK_CLIENT_SECRET,
  randomString: generateRandomString(14),
};

export default keycloakCredentials;
