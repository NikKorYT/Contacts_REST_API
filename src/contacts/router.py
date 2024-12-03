from fastapi import APIRouter, Query, Path, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from config.db import get_db
from src.contacts.repos import ContactRepository
from src.contacts.schemas import Contact, ContactResponse

router = APIRouter()


# Add new contact
@router.post("/contact")
async def create_contact(contact: Contact) -> ContactResponse:
    return ContactResponse(first_name=contact.name, last_name=contact.surname)


# Get all contacts
@router.get("/contact")
async def get_contacts(
    limit: int = Query(10, description="The number of contacts you want to retrieve")
):
    return {"limit": limit}


# Get a specific contact(by ID)
@router.get("/contact/{contact_id}", response_model=ContactResponse)
async def get_contact(
    contact_id: int, db: AsyncSession = Depends(get_db)):
    contact_repo = ContactRepository(db)
    contact = await contact_repo.get_contact(contact_id)
    if not contact:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact