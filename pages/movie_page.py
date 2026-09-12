import allure
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from pages.base_page import BasePage


class MoviePage(BasePage):
    WATCHLIST_BUTTON = (By.XPATH, '//section[@data-testid="search-top-result"]//button[contains(., "Буду смотреть")]')
    WATCHLIST_ACTIVE_BUTTON = (By.XPATH, "//span[text()='В списке']")
    USER_AVATAR = (By.CSS_SELECTOR, "")
    AUTH_MODAL_SELECTOR = ""
    MODAL_CLOSE_SELECTOR = ""
    USER_AVATAR_SELECTOR = ""

    def __init__(self, driver):
        self.driver = driver

    def is_user_logged_in(self) -> bool:
        """Проверяет наличие аватара пользователя."""
        try:
            avatar = self.driver.find_element(By.CSS_SELECTOR, self.USER_AVATAR_SELECTOR)
            return avatar.is_displayed()
        except Exception:
            return False

    def handle_auth_popup_if_present(self, timeout: int = 5):
        """Ждет модальное окно входа и закрывает его, если оно появилось."""
        wait = WebDriverWait(self.driver, timeout)
        try:
            modal = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, self.AUTH_MODAL_SELECTOR)))
            close_btn = modal.find_element(By.CSS_SELECTOR, self.MODAL_CLOSE_SELECTOR)
            close_btn.click()
            # Ждем исчезновения, чтобы следующие шаги не перекрылись этим окном
            wait.until(EC.invisibility_of_element(modal))
        except Exception:
            # Если за 'timeout' секунд окно не появилось — ничего делать не нужно
            pass

    @allure.step("Добавить фильм в список 'Буду смотреть'")
    def add_to_watchlist(self) -> None:
        btn = self.wait.until(
            EC.element_to_be_clickable(self.WATCHLIST_BUTTON)
        )
        btn.click()
        self.wait.until(
            EC.invisibility_of_element_located(self.WATCHLIST_BUTTON)
        )

    @allure.step("Проверить, что фильм добавлен в список")
    def is_in_watchlist(self) -> bool:
        try:
            return self.wait.until(
                EC.visibility_of_element_located(self.WATCHLIST_ACTIVE_BUTTON)
            ).is_displayed()
        except TimeoutException:
            return False

    @allure.step("Проверить видимость аватара пользователя")
    def is_user_logged_in(self) -> bool:
        try:
            return self.wait.until(
                EC.visibility_of_element_located(self.USER_AVATAR)
            ).is_displayed()
        except TimeoutException:
            return False
