import allure

from .base_api_page import BaseAPIPage


class SearchAPIPage(BaseAPIPage):
    SEARCH_ENDPOINT = "/ajax/v1/search"

    @allure.step("Поиск фильма через API: {query}")
    def search_film(self, query: str) -> dict:
        """Возвращает распарсенный JSON ответа."""
        response = self._get(self.SEARCH_ENDPOINT, params={"text": query})
        response.raise_for_status()
        return response.json()