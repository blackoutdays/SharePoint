import requests

#получаем Name и ID файлов с папки с авто ген. токеном

client_id = "a0b22927-fc00-4e93-806c-2f0855b81a87"
client_secret = "jD-8Q~1iDIVSmAcwgPyJHZA1rRGlxP1M6PgSWdsq"
tenant_id = "2d9be5ec-2f5f-4d2f-8a49-67189d7337c5"
scope = 'https://graph.microsoft.com/.default'
token_url = f'https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token'

def get_access_token():
    data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'scope': scope,
        'grant_type': 'client_credentials'
    }
    response = requests.post(token_url, data=data)
    if response.status_code == 200:
        return response.json().get('access_token')
    else:
        raise Exception(f"Error retrieving access token: {response.status_code}, {response.text}")

access_token = get_access_token()

headers = {
    'Authorization': f'Bearer {access_token}',
    'Content-Type': 'application/json'
}

# ID папки QM_all_2023_new
folder_id = "01MTWC63GT2JV7E77SOZFJUB3ENPUFEYJT"
folder_url = f"https://graph.microsoft.com/v1.0/drives/b!aKxyVq6UFUeI-D8MoUwsVENKI0kMsOpIvUW-j41pAbO7NcvkVmEnQI-WV7f7BdWD/items/{folder_id}/children"

response = requests.get(folder_url, headers=headers)

if response.status_code == 200:
    files = response.json()['value']
    for file in files:
        print(f"Name: {file['name']}, ID: {file['id']}")
else:
    print(f"Ошибка при получении файлов: {response.status_code}, {response.text}")