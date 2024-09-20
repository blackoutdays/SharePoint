import requests

#Вывод инфо файла по ID, name, type, size
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

# ID файла, который нужно проверить
file_id = "01MTWC63BFELBTDX6G4RH34SYBWRILGA2K"

# URL для получения информации о файле
info_url = f"https://graph.microsoft.com/v1.0/drives/b!aKxyVq6UFUeI-D8MoUwsVENKI0kMsOpIvUW-j41pAbO7NcvkVmEnQI-WV7f7BdWD/items/{file_id}"

# Выполняем GET запрос для получения информации о файле
response = requests.get(info_url, headers=headers)

if response.status_code == 200:
    file_info = response.json()
    print("Информация о файле:")
    print(f"ID: {file_info['id']}")
    print(f"Название: {file_info['name']}")
    print(f"Тип: {file_info['file']['mimeType']}")
    print(f"Размер: {file_info['size']} байт")
else:
    print(f"Ошибка при получении информации о файле: {response.status_code}, {response.text}")