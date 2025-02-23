import time


from authentication.services.JWTService import JWTService


def test_jwt_services(db_session, user_model, user_session_model):
    # Setup
    jwt_service = JWTService(public_key=user_model.public_key, user_session=user_session_model, db=db_session)

    # Exercise
    jwt_token = jwt_service.get_new_jwt_token()

    # Verify
    assert jwt_token is not None
    assert jwt_service.is_jwt_token_expired(jwt_token) is False

    # Wait 5 sec
    time.sleep(5)

    # Verify
    assert jwt_service.is_jwt_token_expired(jwt_token) is True
