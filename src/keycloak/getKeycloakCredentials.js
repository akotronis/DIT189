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
  kcUrl: 'http://localhost:8080',
  realm: 'DIT189',
  clientId: 'edivorce-frontend',
  clientSecret: 'LlgDke8XNsI9qscSTF59j1yQgFAfsHRB',
  randomString: generateRandomString(14),
};


export default keycloakCredentials;
