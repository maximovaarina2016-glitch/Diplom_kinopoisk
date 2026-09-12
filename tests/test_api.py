import allure
import pytest

import requests

from api_pages.search_api_page import SearchAPIPage

# 1. Параметризованный тест успешного поиска через API
@allure.feature("API: Поиск фильмов по названию")
@pytest.mark.parametrize(
    "film_query,expected_title_part",
    [
        ("Матрица", "Матрица"),
        ("Интерстеллар", "Интерстеллар"),
        ("Начало", "Начало"),
    ],
)
def test_search_film_via_api(
        authorized_api_session: requests.Session, film_query: str, expected_title_part: str
) -> None:
    """
    Проверяет, что API возвращает успешный статус и содержит искомый фильм в выдаче.
    """
    page = SearchAPIPage(authorized_api_session)
    data = page.search_film_by_name(film_query)

    docs = data.get("items", [])
    assert len(docs) > 0, f"По запросу '{film_query}' API не вернул ни одного документа."

    first_film = docs[0]
    name_ru = first_film.get("nameRu", "")
    assert film_query in name_ru, (
        f"Ожидалось частичное совпадение названия '{film_query}', "
        f"получено '{name_ru}'."
    )


# 2. Тест поиска несуществующего фильма (отрицательный сценарий)
@allure.feature("API: Негативные сценарии поиска")
def test_search_non_existent_film_via_api(authorized_api_session: requests.Session) -> None:
    """
    Проверяет корректность обработки пустого результата поисковым эндпоинтом.
    """
    page = SearchAPIPage(authorized_api_session)
    nonsense_query = "asdkjfhaksdjhfaklsdfh12345"
    data = page.search_film_by_name(nonsense_query)

    assert data.get("items") == [], "Для несуществующего запроса API должен вернуть пустой массив документов"

# 3. Поиск Режиссёра по ID
    """
    Проверяет наличие всех обязательных полей у первого человека в списке (обычно это режиссер или главный актер). 
    Используем фильм «Интерстеллар» (ID: 15786).
    """
def test_staff_object_required_fields(authorized_api_session):
    page = SearchAPIPage(authorized_api_session)
    query = "Хэмилтон"
    data = page.search_film_by_director(query)

    assert isinstance(data, list), f"Тип ответа — {type(data)}, ожидался список."
    assert len(data) > 0, f"По запросу '{query}' ничего не найдено."

    first_movie = data[0]

    required_keys = ["nameRu"]
    for query in required_keys:
        assert query in first_movie, f"У первого фильма отсутствует поле '{query}'"

    ru_name = first_movie.get("nameRu")
    if ru_name is not None:
    # Если есть хотя бы одно название, оно должно быть строкой
        assert isinstance(ru_name, str), (
            "Название фильма должно быть строкой"
        )

# 4. Ошибка при отсутствии обязательного параметра filmId
    """
    Параметр filmId обязателен.
    Если его не передать, сервер должен вернуть ошибку 400 Bad Request или 422 Unprocessable Entity.
    """
def test_error_on_missing_film_id(authorized_api_session):
    page = SearchAPIPage(authorized_api_session)
    data = page.search_film_by_name(nonsense_query)

    response = requests.get("https://kinopoiskapiunofficial.tech/api/v1/staff", headers=headers)
    assert response.status_code in [400, 422]
    error_text = str(response.text).lower()
    assert "filmid" in error_text or "required" in error_text

# 5. Поиск известного актёра по части имени.

def test_search_person_by_partial_name(authorized_api_session):
    page = SearchAPIPage(authorized_api_session)

    # Поиск по частичному совпадению
    persons_data = page.search_person_by_name("Ди Каприо")

    assert len(persons_data) > 0, (
        "По запросу 'Ди Каприо' ничего не найдено."
    )

    # Проверяем наличие конкретного человека среди результатов
    found = any(
        p["nameEn"] == "Leonardo DiCaprio" or
        ("nameRu" in p and "Леонардо Ди Каприо" in p.get("nameRu", ""))
        for p in persons_data
    )

    assert found, (
        "В результатах поиска отсутствует Леонардо Ди Каприо.\n"
        f"Найденные имена: {[p['nameEn'] or p.get('nameRu') for p in persons_data]}"
    )