import requests

# Генерирует токен для входа
client_id = "a0b22927-fc00-4e93-806c-2f0855b81a87"
client_secret = "jD-8Q~1iDIVSmAcwgPyJHZA1rRGlxP1M6PgSWdsq"
tenant_id = "2d9be5ec-2f5f-4d2f-8a49-67189d7337c5"
scope = 'https://graph.microsoft.com/.default'
token_url = f'https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token'

data = {
    'client_id': client_id,
    'client_secret': client_secret,
    'scope': scope,
    'grant_type': 'client_credentials'
}

response = requests.post(token_url, data=data)
if response.status_code == 200:
    access_token = response.json().get('access_token')
    print(f"access_token = '{access_token}'")
else:
    print(f"Error retrieving access token: {response.status_code}, {response.text}")


