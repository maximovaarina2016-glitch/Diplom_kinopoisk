import allure

from .base_api_page import BaseAPIPage


class SearchAPIPage(BaseAPIPage):
    SEARCH_ENDPOINT_BY_NAME = "/api/v2.2/films"
    SEARCH_ENDPOINT_BY_ACTOR = "/api/v1/staff"
    SEARCH_ENDPOINT_BY_DIRECTOR = "/api/v1/staff"
    BASE_URL = "https://kinopoiskapiunofficial.tech"

    def __init__(self, api_session): self.session = api_session

    @allure.step("Поиск фильма через API: {query}")
    def search_film_by_name(self, query: str) -> dict:
        """Возвращает распарсенный JSON ответа."""
        response = self._get(self.SEARCH_ENDPOINT_BY_NAME, params={"keyword": query})
        response.raise_for_status()
        return response.json()

    def search_film_by_actor(self, query: str) -> dict:
        """Возвращает распарсенный JSON ответа."""
        response = self._get(self.SEARCH_ENDPOINT_BY_ACTOR, params={"keyword": query})
        response.raise_for_status()
        return response.json()

    def search_film_by_director(self, query: str) -> dict:
        """Возвращает распарсенный JSON ответа."""
        response = self._get(self.SEARCH_ENDPOINT_BY_DIRECTOR, params={"keyword": query})
        response.raise_for_status()
        return response.json()

    def search_without_required_param(self, query: str) -> dict:
        """
        Делает запрос к эндпоинту /api/v1/staff БЕЗ обязательного параметра filmId, чтобы спровоцировать ошибку валидатора.
        Возвращает объект Response, а не распарсенный JSON!
        """
        url = f"{self.BASE_URL}/api/v1/staff"
        return self._get(url)

    def search_person_by_name(self, name_query: str) -> dict:
        """
        Ищет персону по имени через официальный эндпоинт.
        Возвращает распарсенный JSON ответа.
        """

    url = f"{self.BASE_URL}/api/v1/persons"
    params = {"name": name_query}
    response = self.session.get(url, params=params)
    response.raise_for_status()  # Выбросит исключение при статусе >=400 return response.json()