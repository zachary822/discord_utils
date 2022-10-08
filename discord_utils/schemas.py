from typing import Optional

from pydantic import BaseModel, SecretStr


class Token(BaseModel):
    access_token: SecretStr
    expires_in: int
    scope: str
    token_type: str


class Command(BaseModel):
    id: str
    application_id: str
    version: str
    default_permission: Optional[bool]
    default_member_permissions: Optional[str]
    type: int
    name: str
    description: str
