import secrets

from uuid import uuid4

from sqlalchemy.orm import Session

from user.models.user import UserSessionModel


def get_user_session_if_exists(public_key: str, db: Session) -> UserSessionModel | None:
    """
    Get or Create a User Session
    :param public_key:
    :param db:
    :return:
    """
    return db.query(UserSessionModel).filter(UserSessionModel.public_key == public_key).one_or_none()


def create_user_session(public_key: str, db: Session) -> UserSessionModel | None:
    """
    Create a new User Session
    :param public_key:
    :param db:
    :return:
    """
    user_session = UserSessionModel(public_key=public_key)
    db.add(user_session)
    db.commit()
    return user_session


def update_user_session(user_session: UserSessionModel, db: Session) -> UserSessionModel | None:
    """
    Update User Session
    :param user_session:
    :param db:
    :return:
    """
    db.add(user_session)
    db.commit()
    return user_session


def get_or_create_user_session(public_key: str, db: Session) -> UserSessionModel | None:
    """
    Get or Create a User Session
    :param public_key:
    :param db:
    :return:
    """
    user_session = get_user_session_if_exists(public_key=public_key, db=db)
    if not user_session:
        user_session = create_user_session(public_key=public_key, db=db)
    return user_session


def get_new_csrf_user_session(user_session: UserSessionModel, db: Session) -> UserSessionModel | None:
    """
    Update User Session
    :param user_session:
    :param db:
    :return:
    """
    user_session.csrf_token = uuid4()
    db.add(user_session)
    db.commit()
    return user_session


def get_jwt_secret(user_session: UserSessionModel, db: Session) -> str:
    """
    Get JWT Secret
    :param user_session:
    :param db:
    :return:
    """
    jwt_secret = user_session.jwt_secret
    if not jwt_secret:
        jwt_secret = secrets.token_hex(20)
        user_session.jwt_secret = jwt_secret
        db.add(user_session)
        db.commit()

    return jwt_secret


def save_jwt_token(user_session: UserSessionModel, jwt_token: str, db: Session) -> UserSessionModel | None:
    """
    Save JWT Token
    :param user_session:
    :param jwt_token:
    :param db:
    :return:
    """
    user_session.jwt = jwt_token

    db.add(user_session)
    db.commit()
    return user_session
