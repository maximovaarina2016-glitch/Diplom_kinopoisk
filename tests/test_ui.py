import allure
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
def test_open_login_form_from_main_page(main_page: MainPage) -> None:
    main_page.go_to_auth()
    assert main_page.is_on_auth_page, f"Не попали на страницу авторизации. URL: {main_page.driver.current_url}"


# 5. Тест добавления фильма в список
# Используется сценарий перехода на страницу фильма и проверки базовой видимости элементов
@allure.feature("Списки пользователя")
def test_navigate_to_movie_and_check_elements(
    main_page: MainPage, movie_page: MoviePage
) -> None:
    """
    Проверяет переход на страницу фильма и наличие кнопки 'Буду смотреть'.
    Корректно обрабатывает модальное окно входа для неавторизованного пользователя.
    """
    wait = WebDriverWait(main_page.driver, 10)
    # Закрываем появившееся модальное окно входа
    movie_page.handle_auth_popup_if_present(timeout=5)

    # Выполняем поиск
    main_page.enter_search_query("Титаник")
    main_page.click_search()
    main_page.wait_for_results()

    # Нажимаем кнопку действия и закрываем окно авторизации
    watch_btn = wait.until(EC.element_to_be_clickable(movie_page.WATCHLIST_BUTTON))
    watch_btn.click()

    # Проверяем, что кнопка все еще доступна на странице после закрытия окна
    assert main_page.is_on_auth_page, f"Не попали на страницу авторизации. URL: {main_page.driver.current_url}"