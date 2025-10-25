import json
import logging

def is_user_allowed(user_id: int) -> bool:
    """
    Проверяет, разрешён ли пользователь по его ID.

    Args:
        user_id: ID пользователя для проверки

    Returns:
        bool: True если пользователь разрешён, иначе False
    """
    try:
        with open('users.json', 'r') as f:
            data = json.load(f)
            return user_id in data.get('allowed_users', [])
    except FileNotFoundError:
        logging.error("Файл users.json не найден")
        return False
    except json.JSONDecodeError:
        logging.error("Ошибка формата в users.json")
        return False
    except Exception as e:
        logging.error(f"Неизвестная ошибка: {str(e)}")
        return False