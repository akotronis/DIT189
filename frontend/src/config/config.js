import { generateRandomString } from "../utils/keycloak_utils";

//-------------------- API ---------------------

// Base url
export const BASE_URL = process.env.REACT_APP_BACKEND_API_URL;

// Users urls
export const USERS_URL = BASE_URL + '/users?self=1&contains=';
export const MARRIAGES_URL = BASE_URL + '/marriages?in_use=true';
export const NOTARIES_URL = BASE_URL + '/users?&self=0&role=NOTARY&contains=';
export const LAWYERS_URL =
  BASE_URL + '/users?&self=0&role=LAWYER&self=0&contains=';

// Case urls
export const CASES_URL = BASE_URL + '/cases';
export const CASE_UPDATE_URL_SUFFIX = '?confirm=';
export const CASES_FETCH_URL = CASES_URL + '?self=1';


//------------------ KEYCLOAK ------------------

// Keycloak urls
export const KEYCLOAK_URL = process.env.REACT_APP_KEYCLOAK_URL;
export const KEYCLOAK_LOGOUT_URL =
  KEYCLOAK_URL + '/realms/DIT189/protocol/openid-connect/logout';

// Keycloak API

export const keycloakCredentials = {
  kcUrl: KEYCLOAK_URL,
  realm: process.env.REACT_APP_KEYCLOAK_REALM,
  clientId: process.env.REACT_APP_KEYCLOAK_CLIENT_ID,
  clientSecret: process.env.REACT_APP_KEYCLOAK_CLIENT_SECRET,
  randomString: generateRandomString(14),
};

//------------------ NOTIFICATIONS ------------------
export const NOTIFICATIONS_URL = process.env.REACT_APP_NOTIFICATIONS_API_URL+ 'send-mail';