// Base url
export const BASE_URL = 'http://localhost:5000/';

// Users urls
export const USERS_URL = BASE_URL + 'users?self=1&contains=';
export const MARRIAGES_URL = BASE_URL + 'marriages?in_use=true';
export const NOTARIES_URL = BASE_URL + 'users?&self=0&role=NOTARY&contains=';
export const LAWYERS_URL =
  BASE_URL + 'users?&self=0&role=LAWYER&self=0&contains=';

// Case urls
export const CASES_URL = BASE_URL + 'cases';
export const CASE_UPDATE_URL_SUFFIX = '?confirm=';
export const CASES_FETCH_URL = CASES_URL + '?self=1';

// Keycloak urls
export const KEYCLOAK_URL = 'http://localhost:8080';
export const KEYCLOAK_LOGOUT_URL =
  KEYCLOAK_URL + '/realms/DIT189/protocol/openid-connect/logout';
