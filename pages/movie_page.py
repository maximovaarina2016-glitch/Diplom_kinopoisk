import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage


class MoviePage(BasePage):
    WATCHLIST_BUTTON = (By.XPATH, "//span[text()='Буду смотреть']")
    WATCHLIST_ACTIVE_BUTTON = (By.XPATH, "//span[text()='В списке']")
    USER_AVATAR = (By.CSS_SELECTOR, "[data-testid='user-avatar']")

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
