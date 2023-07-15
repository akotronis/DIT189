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

export function generateRandomString(length) {
  const characters = 'abcdefghijklmnopqrstuvwxyz0123456789';
  let randomString = '';

  for (let i = 0; i < length; i++) {
    const randomIndex = Math.floor(Math.random() * characters.length);
    randomString += characters.charAt(randomIndex);
  }

  return randomString;
}