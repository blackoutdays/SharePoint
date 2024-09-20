import requests
import json

#redirect файл в папку
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

drive_id = 'b!aKxyVq6UFUeI-D8MoUwsVENKI0kMsOpIvUW-j41pAbO7NcvkVmEnQI-WV7f7BdWD'
file_id = '01MTWC63CHC3XPUXHHCNHLTDF4UXMCR22C'
destination_folder_id = '01MTWC63GL3VMIKTS2SFEID3UCY3JOUHI6'

# URL для перемещения файла
move_url = f'https://graph.microsoft.com/v1.0/drives/{drive_id}/items/{file_id}'

headers = {
    'Authorization': f'Bearer {access_token}',
    'Content-Type': 'application/json'
}

data = {
    "parentReference": {
        "id": destination_folder_id
    }
}

response = requests.patch(move_url, headers=headers, data=json.dumps(data))

if response.status_code == 200:
    print(f"Файл успешно перемещен в папку: {response.json()['parentReference']['path']}")
else:
    print(f"Ошибка при перемещении файла: {response.status_code}, {response.text}")