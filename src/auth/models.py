from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

from config.db import Base

if TYPE_CHECKING:
    from src.contacts.models import Contact


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String)
    hashed_password: Mapped[str] = mapped_column(String)
    contacts: Mapped[list["Contact"]] = relationship("Contact", back_populates="owner")
    is_active: Mapped[bool] = mapped_column(default=True, nullable=True)