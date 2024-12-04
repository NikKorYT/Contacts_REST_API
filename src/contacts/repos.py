from sqlalchemy import select, or_, func, extract, and_
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta

from src.contacts.models import Contact
from src.contacts.schemas import ContactCreate


class ContactRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_contacts(self, contact_id: int) -> Contact:
        query = select(Contact).where(Contact.id == contact_id)  # Fixed: use select()
        result = await self.session.execute(query)
        return result.scalar_one_or_none()  # Fixed: scalar_one_or_none()

    async def create_contact(self, contact: ContactCreate) -> Contact:
        new_contact = Contact(**contact.model_dump())
        self.session.add(new_contact)
        await self.session.commit()
        await self.session.refresh(new_contact)
        return new_contact

    async def delete_contact(self, contact_id: int):
        query = select(Contact).where(Contact.id == contact_id)
        result = await self.session.execute(query)
        contact = result.scalar_one_or_none()

        if contact:
            await self.session.delete(contact)
            await self.session.commit()
            await self.session.refresh(contact)

        return contact

    async def contact_update(self, contact_id: int, contact_data: ContactCreate):
        query = select(Contact).where(Contact.id == contact_id)
        result = await self.session.execute(query)
        db_contact = result.scalar_one_or_none()

        if db_contact:
            # Update contact with new data
            contact_values = contact_data.model_dump()
            for key, value in contact_values.items():
                setattr(db_contact, key, value)
            await self.session.commit()
            await self.session.refresh(db_contact)

        return db_contact

    async def get_all_contacts(self, skip: int = 0, limit: int = 10) -> list[Contact]:
        query = select(Contact).offset(skip).limit(limit)
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def search_contacts(self, search_text: str) -> list[Contact]:
        query = select(Contact).where(
            or_(
                Contact.name.ilike(f"%{search_text}%"),
                Contact.surname.ilike(f"%{search_text}%"),
                Contact.email.ilike(f"%{search_text}%"),
            )
        )
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def get_upcoming_birthdays(self) -> list[Contact]:
        today = datetime.now().date()
        next_week = today + timedelta(days=7)

        query = select(Contact).where(
            or_(
                and_(
                    extract("month", Contact.date_of_birth) == today.month,
                    extract("day", Contact.date_of_birth) >= today.day,
                    extract("day", Contact.date_of_birth) <= next_week.day,
                ),
                and_(
                    extract("month", Contact.date_of_birth) == next_week.month,
                    extract("day", Contact.date_of_birth) <= next_week.day,
                ),
            )
        )
        result = await self.session.execute(query)
        return list(result.scalars().all())
