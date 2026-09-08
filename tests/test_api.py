import allure
import pytest
from http import HTTPStatus

import requests

from api_pages.search_api_page import SearchAPIPage
from api_pages.auth_api_page import AuthAPIPage


# 1. Параметризованный тест успешного поиска через API
@allure.feature("API: Поиск фильмов")
@pytest.mark.parametrize(
    "film_query,expected_title_part",
    [
        ("Матрица", "Матрица"),
        ("Интерстеллар", "Интерстеллар"),
        ("Начало", "Начало"),
    ],
)
def test_search_film_via_api(
        api_session: requests.Session, film_query: str, expected_title_part: str
) -> None:
    """
    Проверяет, что API возвращает успешный статус и содержит искомый фильм в выдаче.
    """
    page = SearchAPIPage(api_session)
    data = page.search_film(film_query)

    assert data["status"] == "ok", "API вернул ошибку в статусе ответа"
    docs = data.get("docs", [])
    assert len(docs) > 0, f"По запросу '{film_query}' API не вернул ни одного документа."

    first_title = docs[0].get("name") or docs[0].get("enName")
    assert (
            expected_title_part.lower() in first_title.lower()
    ), f"Ожидалось '{expected_title_part}' в ответе, но получено '{first_title}'"


# 2. Тест поиска несуществующего фильма (отрицательный сценарий)
@allure.feature("API: Негативные сценарии поиска")
def test_search_non_existent_film_via_api(api_session: requests.Session) -> None:
    """
    Проверяет корректность обработки пустого результата поисковым эндпоинтом.
    """
    page = SearchAPIPage(api_session)
    nonsense_query = "asdkjfhaksdjhfaklsdfh12345"
    data = page.search_film(nonsense_query)

    assert data["status"] == "ok"
    assert data.get("docs") == [], "Для несуществующего запроса API должен вернуть пустой массив документов"


# 3. Тест проверки заголовков безопасности CORS
@allure.feature("API: Безопасность")
def test_cors_headers_on_search(api_session: requests.Session) -> None:
    """
    Проверяет наличие заголовка Access-Control-Allow-Origin,
    необходимого для работы фронтенда Кинопоиска.
    """
    page = SearchAPIPage(api_session)
    response = page._get(page.SEARCH_ENDPOINT, params={"text": "матрица"})

    assert response.status_code == HTTPStatus.OK
    assert "Access-Control-Allow-Origin" in response.headers, "Заголовок CORS отсутствует"


# 4. Тест получения профиля авторизованного пользователя
@allure.feature("API: Профиль пользователя")
def test_get_authorized_user_profile(authorized_api_session: requests.Session) -> None:
    """
    Проверяет доступ к защищенному эндпоинту /profile после логина.
    """
    page = AuthAPIPage(authorized_api_session)
    profile = page.get_profile()

    assert "id" in profile, "В профиле отсутствует ID пользователя"
    assert isinstance(profile.get("favoriteFilms"), list), "Поле favoriteFilms должно быть списком"


# 5. Тест попытки доступа к профилю без авторизации (проверка прав доступа)
@allure.feature("API: Ограничение доступа")
def test_get_profile_without_auth(api_session: requests.Session) -> None:
    """
    Проверяет, что неавторизованный пользователь получает 401 Unauthorized.
    """
    page = AuthAPIPage(api_session)

    with pytest.raises(requests.exceptions.HTTPError) as exc_info:
        page.get_profile()

    assert exc_info.value.response.status_code == HTTPStatus.UNAUTHORIZED, \
        f"Ожидался статус 401, получен {exc_info.value.response.status_code}"