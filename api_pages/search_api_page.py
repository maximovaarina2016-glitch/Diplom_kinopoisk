import allure
import requests

from .base_api_page import BaseAPIPage


class SearchAPIPage(BaseAPIPage):
    SEARCH_ENDPOINT_BY_NAME = "/api/v2.2/films"
    SEARCH_ENDPOINT_BY_ACTOR = "/api/v1/staff"
    SEARCH_ENDPOINT_BY_DIRECTOR = "/api/v1/persons"
    SEARCH_ENDPOINT_PERSONS = "/api/v1/persons"

    def __init__(self, api_session):
        self.session = api_session


    @allure.step("Поиск фильма через API: {query}")
    def search_film_by_name(self, query: str) -> dict:
        """Возвращает распарсенный JSON ответа."""
        response = self._get(
            self.SEARCH_ENDPOINT_BY_NAME, params={"keyword": query}
        )
        response.raise_for_status()
        return response.json()  # ["items"]

    def search_film_by_actor(self, query: str) -> dict:
        """Возвращает распарсенный JSON ответа."""
        response = self._get(
            self.SEARCH_ENDPOINT_BY_ACTOR, params={"keyword": query}
        )
        response.raise_for_status()
        return response.json()

    def search_person_by_director(self, name_query: str) -> dict:
        """Возвращает распарсенный JSON ответа."""
        response = self._get(
            self.SEARCH_ENDPOINT_PERSONS, params={"name": name_query}
        )

        response.raise_for_status()
        return response.json()

    def search_without_required_param(self) -> requests.Response:
        """
        Делает запрос к эндпоинту /api/v1/staff БЕЗ обязательного параметра filmId, чтобы спровоцировать ошибку валидатора.
        Возвращает ОБЪЕКТ ОТВЕТА (requests.Response). Не вызывает .json(), так как при ошибках сервер может вернуть HTML!
        """
        url = f"{self.BASE_URL}/api/v1/staff"  # Правильный эндпоинт
        return self.session.get(url)

    def search_person_by_keyword(self, name: str) -> list[dict]:
        """
        Ищет персонал по ключевому слову через официальный эндпоинт.
        Возвращает распарсенный JSON ответа (список персон).
        """
        response = self._get(
            self.SEARCH_ENDPOINT_PERSONS, params={"name": name}
        )
        response.raise_for_status()
        return response.json()  # ["items"]
