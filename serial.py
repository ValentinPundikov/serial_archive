import os
import zipfile
import datetime
import requests
import logging

# Настройка логгера
logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')

file_path = ""
output_base_path = ""
bot_token = ''
chat_id = ''

current_datetime = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
output_zip_path = os.path.join(output_base_path, f'serial_logs_{current_datetime}.zip')

with zipfile.ZipFile(output_zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for root, dirs, files in os.walk(file_path):
        for file in files:
            if file.startswith('serial'):
                file_path = os.path.join(root, file)
                zipf.write(file_path, arcname=file)
                logging.info(f"Архивирую файл: {file_path}")

logging.info(f"Архивация завершена. Результат сохранён в: {output_zip_path}")

url = f"https://api.telegram.org/bot{bot_token}/sendDocument"
with open(output_zip_path, 'rb') as file:
    files = {'document': file}
    response = requests.post(url, files=files, data={'chat_id': chat_id})

if response.status_code == 200:
    logging.info("Файл успешно отправлен через Telegram.")
else:
    logging.error("Ошибка при отправке файла через Telegram.")

# Удаление ZIP-файла с устройства
os.remove(output_zip_path)
logging.info(f"Файл {output_zip_path} удален с устройства.")