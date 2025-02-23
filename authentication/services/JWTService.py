import jwt

from datetime import timedelta, datetime, timezone

from sqlalchemy.orm import Session

from settings.hzsettings import get_settings
from user.models.user import UserSessionModel
from user.services.user_session_services import get_jwt_secret, save_jwt_token

settings = get_settings()


class JWTService:

    def __init__(self, public_key: str, user_session: UserSessionModel, db: Session):
        self.public_key = public_key
        self.user_session = user_session
        self.db = db
        self.shared_secret = settings.JWT_SHARED_SECRET
        self.algorithm = settings.JWT_ALGORITHM
        self.expires_in = settings.JWT_EXPIRES_IN

    def _get_jwt_header(self):
        """
        Create the header for the JWT token
        :return:
        """
        return {
            "alg": self.algorithm,
            "typ": "JWT",
        }

    def _payload_jwt_token(self):
        """
        Create the payload for the JWT token
        Common claim types:
        iss (Issuer): Identifies who issued the token.
        sub (Subject): Represents the user or entity the token is about.
        aud (Audience): Specifies the intended recipient.
        exp (Expiration): Defines when the token expires.
        iat (Issued At): Timestamp when the token was created.
        nbf (Not Before): Specifies when the token becomes valid.
        jti (JWT ID): Unique identifier for the token.
        :return:
        """
        return {
            "public_key": self.public_key,
            "iss": "Hypes Zone",
            "sub": "Authentication",
            "aud": "Hypes Zone",
            "exp": datetime.now(timezone.utc) + timedelta(seconds=self.expires_in),
            "iat": f"{datetime.now()}",
            "nbf": f"{datetime.now()}",
            "user_settings": {
                "role": "young ling"
            }
        }

    def get_new_jwt_token(self):
        """
        Based on the public key address and the shared secret create a JWT token
        :return:
        """
        user_session_jwt_secret = get_jwt_secret(user_session=self.user_session, db=self.db)

        jwt_secret = f"{self.shared_secret}{user_session_jwt_secret}"

        jwt_header = self._get_jwt_header()
        jwt_payload = self._payload_jwt_token()
        jwt_header.update(jwt_payload)

        jwt_token = jwt.encode(jwt_header, jwt_secret, self.algorithm)
        save_jwt_token(user_session=self.user_session, jwt_token=jwt_token, db=self.db)

        return jwt_token

    def is_jwt_token_expired(self, jwt_token: str):
        """
        Check if the JWT token is expired
        :param jwt_token:
        :return:
        """
        try:
            jwt.decode(jwt_token, self.shared_secret, algorithms=[self.algorithm])
            return False
        except jwt.ExpiredSignatureError:
            return True
        except jwt.InvalidTokenError:
            return True
        except Exception as e:
            return f"Error processing JWT token: {str(e)}"
