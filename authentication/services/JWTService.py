from typing import Annotated

from fastapi import Depends

from settings.hzsettings import Settings, get_settings

class JWTService():

    def __init__(
            self,
            settings: Annotated[Settings, Depends(get_settings)]
    ):
        self.shared_secret = settings.shared_secret

    def create_jwt_for_public_key(self, public_key: str):
        """
        Based on the public key address and the shared secret create a JWT token
        :param public_key:
        :return:
        """
        pass