from sqlalchemy import Integer, String, Date
from sqlalchemy.orm import Mapped, mapped_column

from config.db import Base

class Contact(Base):
    __tablename__ = 'contacts'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String)
    surname: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String)
    phone: Mapped[int] = mapped_column(Integer)
    date_of_birth: Mapped[Date] = mapped_column(Date)
    additional_info: Mapped[str] = mapped_column(String, nullable=True)
