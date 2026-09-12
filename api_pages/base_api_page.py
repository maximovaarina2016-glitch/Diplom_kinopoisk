import requests
from typing import Dict, Any


class BaseAPIPage:
    BASE_URL = "https://kinopoiskapiunofficial.tech"

    def __init__(self, session: requests.Session) -> None:
        self.session = session

    def _get(self, endpoint: str, params: Dict[str, Any] | None = None) -> requests.Response:
        url = f"{self.BASE_URL}{endpoint}"
        return self.session.get(url, params=params)