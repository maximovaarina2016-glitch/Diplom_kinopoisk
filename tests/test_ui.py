import allure
import pytest
from selenium.webdriver.common.by import By

from pages.main_page import MainPage
from pages.movie_page import MoviePage


# 1. Параметризованный тест успешного поиска
@allure.feature("Поиск фильмов")
@pytest.mark.parametrize(
    "film_query,expected_title_part",
    [
        ("Матрица", "Матрица"),
        ("Интерстеллар", "Интерстеллар"),
        ("Начало", "Начало"),
    ],
)
def test_successful_search(
    main_page: MainPage, film_query: str, expected_title_part: str
) -> None:
    """
    Проверяет, что по валидному запросу находятся результаты
    и первый результат содержит искомое слово.
    """
    main_page.enter_search_query(film_query)
    main_page.click_search()
    main_page.wait_for_results()

    first_title = main_page.get_first_result_title()
    assert (
        expected_title_part.lower() in first_title.lower()
    ), f"Ожидалось '{expected_title_part}' в заголовке, но получено '{first_title}'"


# 2. Тест поиска несуществующего фильма
@allure.feature("Поиск фильмов")
def test_search_non_existent_film(main_page: MainPage) -> None:
    """
    Проверяет отображение заглушки при поиске фильма, которого нет в базе.
    """
    nonsense_query = "asdkjfhaksdjhfaklsdfh12345"
    main_page.enter_search_query(nonsense_query)
    main_page.click_search()
    main_page.wait_for_results()

    assert (
        main_page.is_no_results_message_displayed()
    ), "Сообщение об отсутствии результатов не появилось"


# 3. Тест кликабельности логотипа (возврат на главную)
@allure.feature("Навигация")
def test_logo_redirects_to_homepage(main_page: MainPage) -> None:
    """
    Проверяет, что клик по логотипу Кинопоиска возвращает на главную страницу.
    """
    main_page.enter_search_query("матрица")
    main_page.click_search()
    main_page.wait_for_results()
    main_page.go_to_home()
    assert (
    "/main/" in main_page.driver.current_url
    or main_page.driver.current_url.endswith("/")
    ), f"Логотип не перенаправил на главную. Текущий URL: {main_page.driver.current_url}"


# 4. Тест авторизационного поп-апа (открытие формы входа)
@allure.feature("Авторизация")
def test_open_login_form_from_main_page(main_page: MainPage) -> None:
    """
    Проверяет открытие формы входа/регистрации через иконку профиля.
    """
    main_page.go_to_auth()
    assert (
            "/passport.yandex/" in main_page.driver.current_url
            or main_page.driver.current_url.endswith("/")
    ), f"Логотип не перенаправил на главную. Текущий URL: {main_page.driver.current_url}"


# 5. Тест добавления фильма в список (требует мокирования API или наличия тестового аккаунта)
# Для примера используем сценарий перехода на страницу фильма и проверки базовой видимости элементов
@allure.feature("Списки пользователя")
def test_navigate_to_movie_and_check_elements(
    main_page: MainPage, movie_page: MoviePage
) -> None:
    """
    Проверяет переход на страницу фильма и наличие кнопки 'Буду смотреть'.
    """
    main_page.enter_search_query("Титаник")
    main_page.click_search()
    main_page.wait_for_results()

    first_result_link = main_page.driver.find_element(
        By.CSS_SELECTOR, "[data-testid='search-item'] a"
    )
    first_result_link.click()

    # Теперь мы находимся на странице фильма (MoviePage)
    assert (
        movie_page.is_user_logged_in() is False
    ), "Аватар пользователя не должен быть виден неавторизованному пользователю"

    # Проверяем наличие кнопки действия до логина
    watch_btn = movie_page.driver.find_element(*movie_page.WATCHLIST_BUTTON)
    assert (
        watch_btn.is_displayed()
    ), "Кнопка 'Буду смотреть' отсутствует на странице фильма"
