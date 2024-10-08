import requests
import io
import pandas as pd
import openai

# Генерирует токен, считывает все файлы с папки, обрабатывает с помощью ИИ и сохраняет с новым названием в другую папку

# Конфигурация для получения токена
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
openai.api_key = 'sk-proj-PixdJF0ZmrMTxOP06A7UT3BlbkFJb0rxwyiWvCicwx7lJZ6v'

folder_url = f"https://graph.microsoft.com/v1.0/drives/b!aKxyVq6UFUeI-D8MoUwsVENKI0kMsOpIvUW-j41pAbO7NcvkVmEnQI-WV7f7BdWD/items/children"
source_folder_id = "01MTWC63GT2JV7E77SOZFJUB3ENPUFEYJT"  # Идентификатор папки, от которой берутся все файлы QM_all_2023_new
destination_folder_id = '01MTWC63GL3VMIKTS2SFEID3UCY3JOUHI6'  # Идентификатор целевой папки test
drive_id = 'b!aKxyVq6UFUeI-D8MoUwsVENKI0kMsOpIvUW-j41pAbO7NcvkVmEnQI-WV7f7BdWD'  # Идентификатор диска

headers = {
    'Authorization': f'Bearer {access_token}',
    'Content-Type': 'application/json'
}

def list_files_in_folder(folder_id):
    url = f"https://graph.microsoft.com/v1.0/drives/{drive_id}/items/{folder_id}/children"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json().get('value', [])

def download_file(file_id):
    url = f"https://graph.microsoft.com/v1.0/drives/{drive_id}/items/{file_id}/content"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return io.BytesIO(response.content)

def generate_summary(text):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Прочитай и напиши краткий вывод о содержании следующего текста:\n\n{text}"}
        ],
        max_tokens=150
    )
    return response.choices[0].message['content'].strip()

def process_file(file_stream):
    df = pd.read_excel(file_stream, engine='openpyxl', skiprows=5) # Скипает первые 5 строк ибо там нет названий
    required_columns = ['Дата', 'ID сообщения', 'Сниппет']
    existing_columns = [col for col in required_columns if col in df.columns]
    df = df[existing_columns]
    if 'Сниппет' in df.columns:
        df['Вывод'] = df['Сниппет'].apply(lambda x: generate_summary(x) if pd.notnull(x) else '')
    return df

def upload_file(df, file_name):
    output = io.BytesIO()
    df.to_excel(output, index=False, engine='openpyxl')
    output.seek(0)
    url = f"https://graph.microsoft.com/v1.0/drives/{drive_id}/items/{destination_folder_id}:/{file_name}:/content"
    response = requests.put(url, headers=headers, data=output)
    response.raise_for_status()
    return response.json()

def main():
    global access_token, headers
    try:
        access_token = get_access_token()  # Обновление токена
        headers['Authorization'] = f'Bearer {access_token}'
        files = list_files_in_folder(source_folder_id)
        if not files:
            print("В папке нет файлов для обработки.")
            return

        for file in files:
            file_id = file['id']
            file_name = file['name']
            if file_name.endswith('.xlsx'):  # Обрабатываем только Excel файлы
                print(f"Обработка файла: {file_name}")
                file_stream = download_file(file_id)
                df_processed = process_file(file_stream)
                processed_file_name = f"{file_name.replace('.xlsx', '_processed.xlsx')}"
                upload_response = upload_file(df_processed, processed_file_name)
                print(f"Файл успешно обработан и загружен: {processed_file_name}")
                print(upload_response)
            else:
                print(f"Файл {file_name} не является Excel файлом и будет пропущен.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

if __name__ == "__main__":
    main()