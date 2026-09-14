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
    authorized_api_session: requests.Session,
    film_query: str,
    expected_title_part: str,
) -> None:
    """
    Проверяет, что API возвращает успешный статус и содержит искомый фильм в выдаче.
    """
    page = SearchAPIPage(authorized_api_session)
    data = page.search_film_by_name(film_query)

    docs = data.get("items", [])
    assert (
        len(docs) > 0
    ), f"По запросу '{film_query}' API не вернул ни одного документа."

    first_film = docs[0]
    name_ru = first_film.get("nameRu", "")
    assert film_query in name_ru, (
        f"Ожидалось частичное совпадение названия '{film_query}', "
        f"получено '{name_ru}'."
    )


# 2. Тест поиска несуществующего фильма (отрицательный сценарий)
@allure.feature("API: Негативные сценарии поиска")
def test_search_non_existent_film_via_api(
    authorized_api_session: requests.Session,
) -> None:
    """
    Проверяет корректность обработки пустого результата поисковым эндпоинтом.
    """
    page = SearchAPIPage(authorized_api_session)
    nonsense_query = "asdkjfhaksdjhfaklsdfh12345"
    data = page.search_film_by_name(nonsense_query)

    assert (
        data.get("items") == []
    ), "Для несуществующего запроса API должен вернуть пустой массив документов"

# 3. Поиск Режиссёра по ID
    """
    Проверяет наличие всех обязательных полей у первого человека в списке (обычно это режиссер или главный актер). 
    Используем фильм «Интерстеллар» (ID: 15786).
    """

def test_staff_object_required_fields(authorized_api_session):
    page = SearchAPIPage(authorized_api_session)
    query = "Хэмилтон"
    data = page.search_person_by_director(query)

    persons_list = data.get("items", [])
    assert isinstance(
        persons_list, list
    ), f"Тип данных должен быть список, получен {type(data)}"
    assert len(persons_list) > 0, f"По запросу '{query}' ничего не найдено."

    first_person = persons_list[0]

    required_keys = ["kinopoiskId", "webUrl", "nameRu"]
    for key in required_keys:
        assert (
            key in first_person
        ), f"У первого фильма отсутствует поле '{key}'"

    ru_name = first_person.get("nameRu")
    if ru_name is not None:
        # Если есть хотя бы одно название, оно должно быть строкой
        assert isinstance(ru_name, str), "Название должно быть строкой"
    # Дополнительная проверка: это действительно тот самый человек?
    en_name = first_person.get("nameEn", "").lower()
    assert (
        "hamilton" in en_name or "хэмилтон" in ru_name.lower()
    ), f"Первый объект с ID={first_person['kinopoiskId']} не является персонажем с фамилией Hamilton/Hэмилтон"

# 4. Ошибка при отсутствии обязательного параметра filmId
    """
    Параметр filmId обязателен.
    Если его не передать, сервер должен вернуть ошибку 400 Bad Request или 422 Unprocessable Entity.
    """


def test_error_on_missing_film_id(authorized_api_session):
    page = SearchAPIPage(authorized_api_session)

    response = page.search_without_required_param()

    assert response.status_code in [400], (
        f"ПРИ ОТСУТСТВИИ обязательного параметра filmId ожидался "
        f"статус 400 или 422, получен {response.status_code}."
    )


# 5. Поиск известного актёра по части имени.
@allure.feature("API: Поиск персонала")
def test_search_person_positive(
    authorized_api_session: requests.Session,
) -> None:
    """Проверяет успешный поиск известного актёра."""
    page = SearchAPIPage(authorized_api_session)

    persons_data = page.search_person_by_keyword(
        "Леонардо"
    )  # Менее хрупкий запрос

    assert len(persons_data) > 0, (
        f"API не нашёл ни одного человека по запросу 'Леонардо'. "
        f"Тело ответа: {persons_data}"
    )

    found = any(
        p.get("nameEn", "").lower().startswith("leonardo dicaprio")
        or ("nameRu" in p and "Ди Каприо".casefold() in p["nameRu"].casefold())
        for p in persons_data
    )

    assert found, (
        f"В результатах поиска отсутствует Леонардо Ди Каприо.\n"
        f"Найденные имена: {[p['nameEn'] or p.get('nameRu') for p in persons_data]}"
    )


@allure.feature("API: Обработка ошибок")
def test_search_person_by_partial_name_negative(
    authorized_api_session: requests.Session,
) -> None:
    """Проверяет реакцию на несуществующий/некорректный запрос."""
    page = SearchAPIPage(authorized_api_session)

    # Мы НЕ вызываем .search_person_by_keyword(), потому что он поднимает исключение.
    url = f"{page.BASE_URL}/api/v1/persons?keyword=asdkjfhaksdjhfaklsdfh12345"
    response = authorized_api_session.get(url)

    # Проверка того, что валидатор сработал правильно.
    assert response.status_code == 400, (
        f"ПРИ ОТСУТСТВИИ совпадений ожидался статус 400, получен {response.status_code}."
        f"\nТекст ошибки: {response.text[:100]}..."
    )
