from pydantic import BaseModel


class GuildSchema(BaseModel):
    id: int
    auto_events: bool = False


class ClanSchema(BaseModel):
    tag: str
    guild_id: int


class UserSchema(BaseModel):
    tag: str
    user_id: int
