from pydantic import BaseModel


class SingleChat(BaseModel):
    public_key_initiator: str
    public_key_receiver: str
