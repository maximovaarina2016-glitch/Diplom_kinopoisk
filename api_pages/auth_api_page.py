from typing import Dict, Any

import allure

from .base_api_page import BaseAPIPage


class AuthAPIPage(BaseAPIPage):
    LOGIN_ENDPOINT = "/user/login"
    PROFILE_ENDPOINT = "/user/profile"

    @allure.step("Авторизация пользователя {email}")
    def login(self, email: str, password: str) -> Dict[str, Any]:
        payload = {"email": email, "password": password}
        response = self._post(self.LOGIN_ENDPOINT, json_data=payload)
        response.raise_for_status()
        return response.json()

    @allure.step("Получение профиля пользователя")
    def get_profile(self) -> Dict[str, Any]:
        response = self._get(self.PROFILE_ENDPOINT)
        response.raise_for_status()
        return response.json()