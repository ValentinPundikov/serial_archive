import os
import tarfile
import datetime
import requests
import logging


logging.basicConfig(filename='app.log', filemode='a', format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)


logger = logging.getLogger(__name__)
logger.info("Начало работы скрипта")

file_path = "/etc/point/source/logs/"
output_base_path = "/etc/point/source/logs/"
bot_token = '7282863493:AAGJDZKaPfsDVbPwdgwE6l_Q-OPQ49oA4GM'
chat_id = '869031863'


current_datetime = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
output_tar_gz_path = os.path.join(output_base_path, f'all_logs_{current_datetime}.tar.gz')


try:
    with tarfile.open(output_tar_gz_path, "w:gz") as tar:
        for root, dirs, files in os.walk(file_path):
            for file in files:
                file_path = os.path.join(root, file)
                tar.add(file_path, arcname=file)
                logger.info(f"Архивирую файл: {file_path}")
    logger.info(f"Архивация завершена. Результат сохранён в: {output_tar_gz_path}")
except Exception as e:
    logger.error(f"Ошибка при создании архива: {e}")


try:
    url = f"https://api.telegram.org/bot{bot_token}/sendDocument"
    caption_text = "#2308"
    with open(output_tar_gz_path, 'rb') as file:
        files = {'document': file}
        response = requests.post(url, files=files, data={'chat_id': chat_id, 'caption': caption_text})

    if response.status_code == 200:
        logger.info("Файл успешно отправлен через Telegram.")
    else:
        logger.error("Ошибка при отправке файла через Telegram.")
except Exception as e:
    logger.error(f"Ошибка при отправке файла: {e}")


try:
    os.remove(output_tar_gz_path)
    logger.info(f"Файл {output_tar_gz_path} удален с устройства.")
except Exception as e:
    logger.error(f"Ошибка при удалении файла: {e}")

logger.info("Конец работы скрипта")