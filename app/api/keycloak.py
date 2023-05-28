import os
import requests

class KeycloakAPI:
    def __init__(self):
        self.kc_auth_url = os.getenv('KEYCLOAK_AUTH_URI')
        self.kc_admin_user = os.getenv('KEYCLOAK_ADMIN_USER')
        self.kc_admin_password = os.getenv('KEYCLOAK_ADMIN_PASSWORD')
        self.realm = os.getenv('REALM')
        self.kc_token_template_url = f'{self.kc_auth_url}/realms/' + '{}/protocol/openid-connect/token'
        self.admin_token = self.get_keycloak_admin_access_token()
        # info = self.oidc.user_getinfo(['email', 'sub'])
        # self.admin_email = info.get('email')
        # self.admin_user_id = info.get('sub')


    def get_keycloak_admin_access_token(self):
        '''Get Keycloack Admin token'''

        data = f'client_id=admin-cli&username={self.kc_admin_user}&password={self.kc_admin_password}&grant_type=password'
        admin_token_url = self.kc_token_template_url.format('master')
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        response = requests.post(admin_token_url, headers=headers, data=data)
        if response.status_code == requests.codes.ok:
            return response.json().get('access_token')
        return None

    def create_realm(self):
        headers = {'Content-Type': 'application/json', 'Authorization': f'bearer {self.admin_token}'}
        realms_url = f'{self.kc_auth_url}/admin/realms'
        pass

    def delete_user(self, user_id):
        user_url = f'{self.kc_auth_url}/admin/realms/{self.realm}/users/{user_id}'
        headers = {'Content-Type': 'application/json', 'Authorization': f'bearer {self.admin_token}'}
        response = requests.delete(user_url, headers=headers)
        return response.status_code == 204