from urllib.parse import urlparse

import allure
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage


class MainPage(BasePage):
    SEARCH_FIELD = (By.NAME, "text")
    URL = "https://www.kinopoisk.ru/"
    CLOSE_POPUP_BUTTON = (By.CSS_SELECTOR, '[data-tid="CloseButton"]')

    FIRST_SEARCH_RESULT_TITLE = (
        By.XPATH,
        '//section[@data-testid="search-top-result"]//span[contains(@class, "styles_mainTitle")]',
    )
    SEARCH_RESULTS_WRAPPER = (
        By.CSS_SELECTOR,
        ".styles_searchResultsWrapper__CU2xk",
    )

    def open_page(self) -> None:
        """Открывает главную страницу и закрывает возможные модальные окна."""
        self.driver.get(self.URL)
        self.close_auth_popup()

    @property
    def is_on_auth_page(self) -> bool:
        current = self.driver.current_url
        return "auth" in current or "passport" in current

    @allure.step("Ввести название фильма: {query}")
    def enter_search_query(self, query: str) -> None:
        search_input = self.wait.until(
            EC.visibility_of_element_located(self.SEARCH_FIELD)
        )
        search_input.clear()
        search_input.send_keys(query)

    @allure.step("Нажать кнопку поиска")
    def click_search(self) -> None:
        button = self.driver.find_element(By.XPATH, "//button[text()='Найти']")
        self.driver.execute_script("arguments[0].click();", button)

    @allure.step("Дождаться результатов поиска")
    def wait_for_results(self) -> None:
        self.wait.until(
            EC.presence_of_element_located(self.SEARCH_RESULTS_WRAPPER)
        )

    @allure.step("Закрыть всплывающее окно-подсказку")
    def close_auth_popup(self) -> None:
        try:
            popup_close_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.CLOSE_POPUP_BUTTON)
            )
            popup_close_button.click()
        except (TimeoutException, NoSuchElementException):
            pass

    def get_first_result_title(self) -> str:
        return self.wait.until(
            EC.visibility_of_element_located(self.FIRST_SEARCH_RESULT_TITLE)
        ).text

    def is_no_results_message_displayed(self) -> bool:
        # Примерный селектор сообщения об отсутствии результатов
        no_results_selector = (
            By.XPATH,
            "//div/h2[contains(text(), 'ничего не найдено')]",
        )
        try:
            return self.wait.until(
                EC.visibility_of_element_located(no_results_selector)
            ).is_displayed()
        except TimeoutException:
            return False

    def go_to_home(self) -> None:
        logo = self.driver.find_element(
            By.XPATH, '//a[@data-test-id="next-link"]'
        )
        logo.click()

        # Ждем исчезновения блока результатов поиска
        self.wait.until(
            EC.invisibility_of_element_located(self.SEARCH_RESULTS_WRAPPER)
        )

    def go_to_auth(self) -> None:
        logo = self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, '//button[@data-testid="loginHeaderButton"]')
            )
        )
        logo.click()

    def is_on_home_page(self) -> bool:
        """
        Проверяет, что мы на главной странице Кинопоиска.
        Учитывает, что главная может быть как '/', так и '/main/'.
        """
        path = urlparse(self.driver.current_url).path
        return path in ("/", "/main/") or path.startswith("/main/")


    def current_url(self) -> str:
        """
        Возвращает текущий URL. Нужен только для сообщений об ошибках в тестах.
        """
        return self.driver.current_url
