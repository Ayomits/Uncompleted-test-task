from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, declared_attr
from datetime import datetime


class Base(DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True)

    @declared_attr
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}"
