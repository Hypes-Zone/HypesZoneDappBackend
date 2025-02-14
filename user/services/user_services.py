from sqlalchemy.orm import Session

from user.models.user import UserModel


def get_user_if_exists(public_key: str, db: Session) -> UserModel | None:
    """
    Returns the UserModel if exists, else returns None
    :param public_key:
    :param db:
    :return:
    """
    return db.query(UserModel).filter(UserModel.public_key == public_key).one_or_none()


def create_user(public_key: str, db: Session) -> UserModel | None:
    """
    Create a new User
    :param public_key:
    :param db:
    :return:
    """
    user = UserModel(public_key=public_key)
    db.add(user)
    db.commit()
    return user


def get_or_create_user(public_key: str, db: Session) -> UserModel | None:
    """
    Get or Create a User
    :param public_key:
    :param db:
    :return:
    """
    user = get_user_if_exists(public_key=public_key, db=db)
    if not user:
        user = create_user(public_key=public_key, db=db)
    return user
