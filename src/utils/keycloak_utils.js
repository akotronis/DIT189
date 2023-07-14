import jwt_decode from "jwt-decode";
export function decodeAccessToken(accessToken) {
  try {
    const decodedToken = jwt_decode(accessToken);
    return decodedToken;
  } catch (error) {
    console.error('Error decoding access token:', error);
    return null;
  }
}
