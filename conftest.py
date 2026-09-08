from typing import Generator

import pytest
import allure
import requests
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options

@pytest.fixture(scope="function")
def api_session() -> requests.Session:
    """ Базовая сессия для неавторизованных запросов к API.
    """
    with requests.Session() as session:
        session.headers.update({"User-Agent": "QA-Automation-Bot/1.0"})
        yield session

@pytest.fixture
def driver() -> Generator[WebDriver, None, None]:
    """Создаёт и настраивает браузер перед тестом, закрывает его после
    теста (даже если тест упал)."""

    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()

@pytest.fixture
def main_page(driver) -> "MainPage":
    from pages.main_page import MainPage
    page = MainPage(driver)
    page.open_page()
    return page

@pytest.fixture
def movie_page(driver) -> "MoviePage":
    from pages.movie_page import MoviePage
    return MoviePage(driver)

@pytest.fixture(scope="function")
def api_session() -> requests.Session:
    """
    Базовая сессия для неавторизованных запросов к API.
    """
    with requests.Session() as session:
        session.headers.update({"User-Agent": "QA-Automation-Bot/1.0"})
        yield session

@pytest.fixture(scope="function")
def authorized_api_session(api_session: requests.Session) -> requests.Session:
    """
    Авторизованная сессия.
    Данные лучше выносить в переменные окружения (.env).
    """
    from api_pages.auth_api_page import AuthAPIPage

    auth_page = AuthAPIPage(api_session)

    # В реальном проекте используйте os.getenv или конфиги
    credentials = {
        "email": "maximova.arina2016@gmail.com",
        "password": "xLjzS3fJ3k!.FQ#"
    }

    token_data = auth_page.login(**credentials)

    # Предполагаем, что токен приходит в поле 'token'
    if token_data.get("token"):
        api_session.headers.update({"Authorization": f"Bearer {token_data['token']}"})

    yield api_session