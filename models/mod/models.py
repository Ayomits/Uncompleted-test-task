from core import Base
from datetime import datetime
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import TIMESTAMP, BigInteger, Integer


class Mute(Base):
    user_id: Mapped[int] = mapped_column(type_=BigInteger, unique=True)
    end_mute: Mapped[int] = mapped_column(type_=BigInteger)

class Warns(Base):
    user_id: Mapped[int] = mapped_column(type_=BigInteger, unique=True)
    count: Mapped[int] = mapped_column(type_=Integer, default=0)

class MuteSettings(Base):
    guild_id: Mapped[int] = mapped_column(type_=BigInteger, unique=True, default=0)
    role_id: Mapped[int] = mapped_column(type_=BigInteger, unique=True, default=0)