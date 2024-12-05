from fastapi import APIRouter, Query, Path, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from config.db import get_db
from src.contacts.repos import ContactRepository
from src.contacts.schemas import Contact, ContactResponse, ContactCreate


router = APIRouter()

# Add new contact
@router.post("/", response_model=ContactResponse)
async def create_contact(contact: ContactCreate, db: AsyncSession = Depends(get_db)):
    contact_repo = ContactRepository(db)
    return await contact_repo.create_contact(contact)


# Get a specific contact(by ID)
@router.get("/{contact_id}", response_model=ContactResponse)
async def get_contact(contact_id: int, db: AsyncSession = Depends(get_db)):
    contact_repo = ContactRepository(db)
    contact = await contact_repo.get_contacts(contact_id)
    if not contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )
    return contact


@router.delete("/{contact_id}", response_model=ContactResponse)
async def delete_contact(contact_id: int, db: AsyncSession = Depends(get_db)):
    contact_repo = ContactRepository(db)
    contact = await contact_repo.delete_contact(contact_id)
    if not contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )
    return contact


@router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact(
    contact_id: int, contact: ContactCreate, db: AsyncSession = Depends(get_db)
):
    contact_repo = ContactRepository(db)
    contact = await contact_repo.contact_update(contact_id, contact)
    if not contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )
    return contact


@router.get("/", response_model=List[ContactResponse])
async def get_contacts(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1),
    db: AsyncSession = Depends(get_db)
):
    contact_repo = ContactRepository(db)
    contacts = await contact_repo.get_all_contacts(skip, limit)
    return contacts

@router.get("/search/", response_model=List[ContactResponse])
async def search_contacts(
    query: str = Query(..., min_length=2, description="Search by name, surname or email"),
    db: AsyncSession = Depends(get_db)
):
    contact_repo = ContactRepository(db)
    contacts = await contact_repo.search_contacts(query)
    return contacts

@router.get("/birthdays/", response_model=List[ContactResponse])
async def upcoming_birthdays(db: AsyncSession = Depends(get_db)):
    contact_repo = ContactRepository(db)
    contacts = await contact_repo.get_upcoming_birthdays()
    return contacts
