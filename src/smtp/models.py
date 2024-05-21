from pydantic import BaseModel


class MsgDataModel(BaseModel):
    from_email: str
    to_email: str
    subject: str | None = None
    text: str | None = None
    html: str | None = None
