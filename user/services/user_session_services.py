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
