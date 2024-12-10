from sqlalchemy import select, or_, func, extract, and_
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta

from src.contacts.models import Contact
from src.contacts.schemas import ContactCreate


class ContactRepository:
    """Repository for managing Contact entities in the database.

    This class handles all database operations related to contacts including
    creating, reading, updating and deleting contact records.

    Attributes:
        session (AsyncSession): The database session for performing operations.
    """
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_contacts(self, contact_id: int) -> Contact:
        """Retrieve a contact by its ID.

        Args:
            contact_id (int): The unique identifier of the contact.

        Returns:
            Contact: The found contact object or None if not found.
        """
        query = select(Contact).where(Contact.id == contact_id)  # Fixed: use select()
        result = await self.session.execute(query)
        return result.scalar_one_or_none()  # Fixed: scalar_one_or_none()

    async def create_contact(self, contact: ContactCreate, owner_id: int) -> Contact:
        """Create a new contact in the database.

        Args:
            contact (ContactCreate): The contact data to create.
            owner_id (int): The ID of the user who owns this contact.

        Returns:
            Contact: The newly created contact object.
        """
        new_contact = Contact(**contact.model_dump(), owner_id=owner_id)
        self.session.add(new_contact)
        await self.session.commit()
        await self.session.refresh(new_contact)
        return new_contact

    async def delete_contact(self, contact_id: int):
        """Delete a contact from the database.

        Args:
            contact_id (int): The ID of the contact to delete.

        Returns:
            bool: True if contact was deleted, False if not found
        """
        contact = await self.get_contacts(contact_id)
        if contact:
            await self.session.delete(contact)
            await self.session.commit()
        return contact

    async def contact_update(self, contact_id: int, contact_data: ContactCreate):
        """Update an existing contact.

        Args:
            contact_id (int): The ID of the contact to update
            contact (ContactUpdate): The new contact data

        Returns:
            Contact: The updated contact object
        """
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

    async def get_all_contacts(self, user_id: int, skip: int = 0, limit: int = 100) -> list[Contact]:
        """Retrieve all contacts for a specific user with pagination.

        Args:
            user_id (int): The ID of the user whose contacts to retrieve
            skip (int, optional): Number of records to skip. Defaults to 0.
            limit (int, optional): Maximum number of records to return. Defaults to 100.

        Returns:
            list[Contact]: List of Contact objects belonging to the user
        """
        query = (
            select(Contact)
            .where(Contact.owner_id == user_id)
            .offset(skip)
            .limit(limit)
        )
        result = await self.session.execute(query)
        return result.scalars().all()

    async def search_contacts(self, search_text: str, user_id: int) -> list[Contact]:
        """Search contacts by name, email or phone.

        Args:
            query (str): Search query string
            owner_id (int): ID of contacts owner

        Returns:
            List[Contact]: List of matching contacts
        """
        query = (
            select(Contact)
            .where(
                and_(
                    Contact.owner_id == user_id,
                    or_(
                        Contact.name.ilike(f"%{search_text}%"),
                        Contact.surname.ilike(f"%{search_text}%"),
                        Contact.email.ilike(f"%{search_text}%"),
                    ),
                )
            )
        )
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_upcoming_birthdays(self, user_id: int) -> list[Contact]:
        """Get contacts with birthdays in the next 7 days.

        Returns:
            List[Contact]: List of contacts with upcoming birthdays
        """
        today = datetime.now().date()
        next_week = today + timedelta(days=7)

        query = (
            select(Contact)
            .where(
                and_(
                    Contact.owner_id == user_id,
                    or_(
                        and_(
                            extract("month", Contact.date_of_birth) == today.month,
                            extract("day", Contact.date_of_birth) >= today.day,
                        ),
                        and_(
                            extract("month", Contact.date_of_birth) == next_week.month,
                            extract("day", Contact.date_of_birth) <= next_week.day,
                        ),
                    ),
                )
            )
        )
        result = await self.session.execute(query)
        return result.scalars().all()
