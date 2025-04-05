import logging
import aiohttp
import json

logger = logging.getLogger(__name__)

async def send_to_database(items: list) -> bool:
    """Отправляет новости в базу данных через API"""
    logger.info(f"[{items[0].get('author', 'Unknown')}] Отправка пакета из {len(items)} новостей")
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                'http://djangoapp:8000/api-dev/news/',
                json=items,
                headers={'Content-Type': 'application/json'}
            ) as response:
                if response.status == 201:  # Успешное создание
                    logger.info(f"Успешно отправлено {len(items)} новостей")
                    return True
                else:
                    logger.error(f"Ошибка при отправке новостей: {response.status}")
                    error_text = await response.text()
                    logger.error(f"Ответ сервера: {error_text}")
                    return False
                    
    except Exception as e:
        logger.error(f"Ошибка при отправке данных в БД: {str(e)}")
        return False