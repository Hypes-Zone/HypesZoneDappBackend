import base58
import nacl.signing

from sqlalchemy.orm import Session

from user.services import user_session_services

from settings.hzsettings import get_settings
settings = get_settings()


class Web3AuthService:

    def __init__(
            self,
            public_key: str,
            signature: str,
            original_message: str,
            db: Session,
    ):
        self.public_key = public_key
        self.signature = signature
        self.original_message = original_message
        self.db = db
        self.shared_secret = settings.SHARED_SECRET

    def verify_signed_message(self):
        """
        Verify if the public_key user has signed the secret message
        :return:
        """
        # Get the user session
        user_session = user_session_services.get_or_create_user_session(
            public_key=self.public_key, db=self.db
        )

        message =  self.original_message.replace("XXX", str(user_session.csrf_token))

        try:
            # Decode public key and signature from Base58
            public_key_bytes = base58.b58decode(self.public_key)
            signature_bytes = base58.b58decode(self.signature)

            # Convert public key to verify key format
            verify_key = nacl.signing.VerifyKey(public_key_bytes)

            # Verify the signature
            try:
                verify_key.verify(message.encode(), signature_bytes)
                user_session.signed_message = self.signature
                user_session_services.update_user_session(user_session=user_session, db=self.db)
                return True
            except nacl.exceptions.BadSignatureError:
                return False

        except Exception as e:
            return f"Error processing signature: {str(e)}"