from fastapi import HTTPException
import requests


class UserService:
    def __init__(self, endpoint: str):
        self.endpoint = endpoint

    def user_contains_role(self, jwttoken: str, roleName: str) -> bool:
        try:
            response = requests.get(self.endpoint + "userContainsRole", data={"roleName": roleName},
                                    headers={"accessToken": jwttoken})
        except:
            raise HTTPException(408, "Cannot reach " + self.endpoint)
        hasAccess = response.json()
        return hasAccess


class PaymentService:
    def __init__(self, endpoint: str):
        self.endpoint = endpoint

    def make_payment(self, txService: str, jwttoken: str):
        try:
            response = requests.post(self.endpoint + "api/v1/pay", data={"txService": txService},
                                     headers={"accessToken": jwttoken})
        except:
            raise HTTPException(408, "Cannot reach " + self.endpoint)
        return response.json()


class NotificationService:
    def __init__(self, endpoint: str):
        self.endpoint = endpoint

    def notify(self, jwttoken: str):
        try:
            response = requests.get(self.endpoint + "notify", headers={"accessToken": jwttoken})
        except:
            raise HTTPException(408, "Cannot reach " + self.endpoint)
        return response.json()


class StoreService:
    def __init__(self, endpoint: str):
        self.endpoint = endpoint

    def check_price(self, product_name: str, jwttoken: str):
        try:
            response = requests.get(self.endpoint + "products/" + product_name, headers={"accessToken": jwttoken})
        except:
            raise HTTPException(408, "Cannot reach " + self.endpoint)
        return response.json()
