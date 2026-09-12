from typing import Generator, Any

import pytest
import requests
from requests import Session
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver

from pages.main_page import MainPage
from pages.movie_page import MoviePage


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

@pytest.fixture(scope="function")
def api_session() -> requests.Session:
    """
    Базовая сессия для неавторизованных запросов к API.
    """
    with requests.Session() as session:
        session.headers.update({"User-Agent": "QA-Automation-Bot/1.0"})
        yield session

@pytest.fixture
def movie_page(driver) -> "MoviePage":
    from pages.movie_page import MoviePage
    return MoviePage(driver)

@pytest.fixture(scope="function")
def authorized_api_session(api_session: requests.Session) -> Generator[Session, Any, None]:
    """
    Авторизованная сессия.
    Данные лучше выносить в переменные окружения (.env).
    """
    api_session.headers.update({"X-API-KEY": "a5ddce49-228c-4386-b346-3d5819c45f55"})

    yield api_session
