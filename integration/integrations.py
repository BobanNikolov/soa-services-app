from fastapi import HTTPException
import requests


class UserService:
    def __init__(self, endpoint: str):
        self.endpoint = endpoint

    def userContainsRole(self, jwttoken: str, roleName: str) -> bool:
        try:
            response = requests.get(self.endpoint + "userContainsRole", data={"roleName": roleName},
                                    headers={"accessToken": jwttoken})
        except:
            raise HTTPException(408, "Cannot reach " + self.endpoint)
        hasAccess = response.json()
        return hasAccess

