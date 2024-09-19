import requests
import io
import pandas as pd
import openai

access_token = 'eyJ0eXAiOiJKV1QiLCJub25jZSI6IlNDM25YeW1LSW1qTTFLNk9TbFU4c2ozNE1OcDZ1U1hURFpuUm5oTGVCSzgiLCJhbGciOiJSUzI1NiIsIng1dCI6Ikg5bmo1QU9Tc3dNcGhnMVNGeDdqYVYtbEI5dyIsImtpZCI6Ikg5bmo1QU9Tc3dNcGhnMVNGeDdqYVYtbEI5dyJ9.eyJhdWQiOiJodHRwczovL2dyYXBoLm1pY3Jvc29mdC5jb20iLCJpc3MiOiJodHRwczovL3N0cy53aW5kb3dzLm5ldC8yZDliZTVlYy0yZjVmLTRkMmYtOGE0OS02NzE4OWQ3MzM3YzUvIiwiaWF0IjoxNzI2NzQ2MTYzLCJuYmYiOjE3MjY3NDYxNjMsImV4cCI6MTcyNjc1MDA2MywiYWlvIjoiRTJkZ1lGQ2J1T1NoMmJrdHEyTENuNTU0K0V1ckF3QT0iLCJhcHBfZGlzcGxheW5hbWUiOiJ0ZXN0IiwiYXBwaWQiOiJhMGIyMjkyNy1mYzAwLTRlOTMtODA2Yy0yZjA4NTViODFhODciLCJhcHBpZGFjciI6IjEiLCJpZHAiOiJodHRwczovL3N0cy53aW5kb3dzLm5ldC8yZDliZTVlYy0yZjVmLTRkMmYtOGE0OS02NzE4OWQ3MzM3YzUvIiwiaWR0eXAiOiJhcHAiLCJvaWQiOiJjMDljZTA2MS05Y2Q2LTQ2NTEtODM5Yi01YTY3ZjlmM2QwOTIiLCJyaCI6IjAuQVU0QTdPV2JMVjh2TDAyS1NXY1luWE0zeFFNQUFBQUFBQUFBd0FBQUFBQUFBQUJPQUFBLiIsInJvbGVzIjpbIkZpbGVzLlJlYWRXcml0ZS5BcHBGb2xkZXIiLCJTaXRlcy5TZWxlY3RlZCIsIkZpbGVzLlNlbGVjdGVkT3BlcmF0aW9ucy5TZWxlY3RlZCIsIlNpdGVzLlJlYWQuQWxsIiwiU2l0ZXMuUmVhZFdyaXRlLkFsbCIsIlNpdGVzLk1hbmFnZS5BbGwiLCJGaWxlcy5SZWFkV3JpdGUuQWxsIiwiRmlsZXMuUmVhZC5BbGwiLCJTaXRlcy5GdWxsQ29udHJvbC5BbGwiXSwic3ViIjoiYzA5Y2UwNjEtOWNkNi00NjUxLTgzOWItNWE2N2Y5ZjNkMDkyIiwidGVuYW50X3JlZ2lvbl9zY29wZSI6IkVVIiwidGlkIjoiMmQ5YmU1ZWMtMmY1Zi00ZDJmLThhNDktNjcxODlkNzMzN2M1IiwidXRpIjoiWUFxcWowMzZhVXk4UW43ZTNBb1lBQSIsInZlciI6IjEuMCIsIndpZHMiOlsiMDk5N2ExZDAtMGQxZC00YWNiLWI0MDgtZDVjYTczMTIxZTkwIl0sInhtc19pZHJlbCI6IjcgMTQiLCJ4bXNfdGNkdCI6MTY0NDkzMDUzNH0.QKgsp6UW1haLbONmskWPPsI_pUW5n7RHvQOoDIiVer4xNGPMl4KUnvHVSEjK8Q8eY96oHHDgp4x3ktKqrWuOjCUKlaElEu8wllAEPvMg2liM6CjSBpVlMliSnvu376RBaOS-LxX1vQxZw6jpKBMaLOHm25L0dfjPR3sR_yl_NdFGDoTv8R_Txs9meAjLDQHS0cUxYYzyipTEunSyLvmfcLh_v4geY8H2_WUrcHaN9kVV7AiX1YM0nb6KFtAROUccW088g6rsDyKDcWvLstuXnX-oT8hBR_UrCYmqg-PPu5G2T_X3pUcyuCjQzQziozHH1EmKYsv0uG9P1y1J4o0o9A'
openai.api_key = 'sk-proj-PixdJF0ZmrMTxOP06A7UT3BlbkFJb0rxwyiWvCicwx7lJZ6v'

folder_url = f"https://graph.microsoft.com/v1.0/drives/b!aKxyVq6UFUeI-D8MoUwsVENKI0kMsOpIvUW-j41pAbO7NcvkVmEnQI-WV7f7BdWD/items/children"
source_folder_id = "01MTWC63GT2JV7E77SOZFJUB3ENPUFEYJT" #Идентификатор папки, от которой берутся все файлы
destination_folder_id = '01MTWC63GL3VMIKTS2SFEID3UCY3JOUHI6'  #Идентификатор целевой папки test, куда будут загружаться обработанные файлы
drive_id = 'b!aKxyVq6UFUeI-D8MoUwsVENKI0kMsOpIvUW-j41pAbO7NcvkVmEnQI-WV7f7BdWD'  #Идентификатор диска

headers = {
    'Authorization': f'Bearer {access_token}',
    'Content-Type': 'application/json'
}

# Получение списка файлов из папки
def list_files_in_folder(folder_id):
    url = f"https://graph.microsoft.com/v1.0/drives/{drive_id}/items/{folder_id}/children"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json().get('value', [])

# Загрузка файла из SharePoint/OneDrive
def download_file(file_id):
    url = f"https://graph.microsoft.com/v1.0/drives/{drive_id}/items/{file_id}/content"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return io.BytesIO(response.content)

# Генерация с использованием ChatGPT (gpt-3.5-turbo)
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

# Чтение и обработка файла
def process_file(file_stream):
    df = pd.read_excel(file_stream, engine='openpyxl', skiprows=5) #скипает первые 5 строк ибо там нет названий
    required_columns = ['Дата', 'ID сообщения', 'Сниппет']
    existing_columns = [col for col in required_columns if col in df.columns]
    df = df[existing_columns]
    if 'Сниппет' in df.columns:
        df['Вывод'] = df['Сниппет'].apply(lambda x: generate_summary(x) if pd.notnull(x) else '')
    return df

# Сохранение обработанного файла обратно в SharePoint/OneDrive
def upload_file(df, file_name):
    output = io.BytesIO()
    df.to_excel(output, index=False, engine='openpyxl')
    output.seek(0)
    url = f"https://graph.microsoft.com/v1.0/drives/{drive_id}/items/{destination_folder_id}:/{file_name}:/content"
    response = requests.put(url, headers=headers, data=output)
    response.raise_for_status()
    return response.json()

# Основной процесс
def main():
    try:
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