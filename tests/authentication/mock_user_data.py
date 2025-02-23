import pytest

from user.models.user import UserModel, UserSessionModel


@pytest.fixture()
def user_model(db_session) -> UserModel:
    user_model = UserModel(public_key="test_public_key")
    db_session.add(user_model)
    db_session.commit()
    return user_model


@pytest.fixture()
def user_session_model(db_session, user_model) -> UserSessionModel:
    user_session_model = UserSessionModel(public_key=user_model.public_key)
    db_session.add(user_session_model)
    db_session.commit()
    return user_session_model
