from typing import Type

from sqlalchemy.orm import Session

from chat.models.single_chats import SingleChatModel


def get_all_initiator_single_chats(public_key: str, db: Session) -> list[Type[SingleChatModel]]:
    """
    Get all single chats initiated by the user
    :param public_key:
    :param db:
    :return:
    """
    return db.query(SingleChatModel).filter(
        SingleChatModel.public_key_user_initiator == public_key
    ).all()


def get_all_receiver_single_chats(public_key: str, db: Session) -> list[Type[SingleChatModel]]:
    """
    Get all single chats received by the user
    :param public_key:
    :param db:
    :return:
    """
    return db.query(SingleChatModel).filter(
        SingleChatModel.public_key_user_receiver == public_key
    ).all()


def get_single_chat_if_exists(public_key_initiator: str, public_key_receiver: str,
                              db: Session) -> SingleChatModel | None:
    """
    Returns the SingleChatModel if exists, else returns None
    :param public_key_initiator:
    :param public_key_receiver:
    :param db:
    :return:
    """
    return db.query(SingleChatModel).filter(
        SingleChatModel.public_key_user_initiator == public_key_initiator
    ).filter(
        SingleChatModel.public_key_user_receiver == public_key_receiver
    ).one_or_none()


def create_single_chat_if_none_exists(public_key_initiator: str, public_key_receiver: str, db: Session) -> tuple[
    SingleChatModel, bool]:
    """
    Create a new Single Chat if none exists
    :param public_key_initiator:
    :param public_key_receiver:
    :param db:
    :return:
    """
    single_chat = get_single_chat_if_exists(
        public_key_initiator=public_key_initiator, public_key_receiver=public_key_receiver, db=db
    )

    if single_chat:
        return single_chat, False

    single_chat = SingleChatModel(
        public_key_user_initiator=public_key_initiator, public_key_user_receiver=public_key_receiver,
        chat_accepted=True
    )
    db.add(single_chat)
    db.commit()
    return single_chat, True
