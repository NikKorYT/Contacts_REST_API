from sqlalchemy import Integer, String, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

from config.db import Base

if TYPE_CHECKING:
    from src.auth.models import User

class Contact(Base):
    __tablename__ = 'contacts'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String)
    surname: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String)
    phone: Mapped[int] = mapped_column(Integer)
    date_of_birth: Mapped[Date] = mapped_column(Date)
    additional_info: Mapped[str] = mapped_column(String, nullable=True)
    owner_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=True)
    owner: Mapped["User"] = relationship("User", back_populates="contacts")