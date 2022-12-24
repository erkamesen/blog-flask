from enum import Enum
import requests

class Condition(Enum):

    WARNING = "⚠"
    ERROR = "💀"

class Logger:

    def __init__(self, token, chat_id):
        self._token = token
        self._chat_id = chat_id
        self._url = f"https://api.telegram.org/bot{token}/"

    def log(self, message, condition=None):
        text = message
        if condition is not None:
            text = f"{condition.value} {text}"

        url = self._url + "sendMessage"
        resp = requests.post(
            url=url,
            params = {
                "chat_id": self._chat_id,
                "text": text
            }
        )
        resp.raise_for_status()

    def warning(self, message):
        self.log(message, Condition.WARNING)

    def error(self, message):
        self.log(message, Condition.ERROR)
        
        
        
""" logger = Logger(token="5714462131:AAEaALnkxrDlHEY3qxY-CTJtBRgeNAuP6pY", chat_id="5641288499")
logger.warning(message="HELOOOOO") """