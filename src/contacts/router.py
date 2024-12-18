from fastapi import APIRouter, Query, Path, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from fastapi_limiter.depends import RateLimiter

from config.db import get_db
from src.auth.models import User
from src.auth.utils import get_current_user
from src.contacts.repos import ContactRepository
from src.contacts.schemas import Contact, ContactResponse, ContactCreate, ContactUpdate


router = APIRouter()


# Add new contact
@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED, 
    dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def create_contact(
    contact: ContactCreate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Create a new contact for the authenticated user.

    Args:
        contact (ContactCreate): Contact data to create
        user (User): Current authenticated user from token
        db (AsyncSession): Database session

    Returns:
        ContactResponse: Created contact data

    Raises:
        HTTPException: If rate limit exceeded
    """
    contact_repo = ContactRepository(db)

    return await contact_repo.create_contact(contact, user.id)


# Get a specific contact(by ID)
@router.get("/{contact_id}", response_model=ContactResponse)
async def get_contact(
    contact_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Retrieve a specific contact by ID.

    Args:
        contact_id (int): ID of contact to retrieve
        db (AsyncSession): Database session
        user (User): Current authenticated user

    Returns:
        ContactResponse: Contact data if found

    Raises:
        HTTPException: If contact not found or doesn't belong to user
    """
    contact_repo = ContactRepository(db)
    contact = await contact_repo.get_contacts(contact_id)

    if not contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact not found"
        )

    if contact.owner_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this contact"
        )

    return contact


@router.delete("/{contact_id}", response_model=ContactResponse)
async def delete_contact(
    contact_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Delete a specific contact.

    Args:
        contact_id (int): ID of contact to delete
        user (User): Current authenticated user
        db (AsyncSession): Database session

    Raises:
        HTTPException: If contact not found or doesn't belong to user
    """
    contact_repo = ContactRepository(db)
    contact = await contact_repo.get_contacts(contact_id)

    if not contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact not found"
        )

    if contact.owner_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this contact"
        )

    await contact_repo.delete_contact(contact_id)
    return contact


@router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact(
    contact_id: int,
    contact_data: ContactUpdate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Update an existing contact.

    Args:
        contact_id (int): ID of contact to update
        contact (ContactUpdate): New contact data
        user (User): Current authenticated user
        db (AsyncSession): Database session

    Returns:
        ContactResponse: Updated contact data

    Raises:
        HTTPException: If contact not found or doesn't belong to user
    """
    contact_repo = ContactRepository(db)
    contact = await contact_repo.get_contacts(contact_id)

    if not contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact not found"
        )

    if contact.owner_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this contact"
        )

    updated_contact = await contact_repo.contact_update(contact_id, contact_data)
    return updated_contact


@router.get("/", response_model=List[ContactResponse],
    dependencies=[Depends(RateLimiter(times=20, seconds=60))])
async def get_contacts(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get paginated list of all contacts for the authenticated user.

    Args:
        skip (int): Number of records to skip for pagination
        limit (int): Maximum number of records to return
        user (User): Current authenticated user
        db (AsyncSession): Database session

    Returns:
        List[ContactResponse]: List of contacts
    """
    contact_repo = ContactRepository(db)
    contacts = await contact_repo.get_all_contacts(user.id, skip, limit)
    return contacts


@router.get("/search/", response_model=List[ContactResponse],
    dependencies=[Depends(RateLimiter(times=30, seconds=60))])
async def search_contacts(
    query: str = Query(..., min_length=2, description="Search by name, surname, or email"),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Search contacts by name, surname, or email.
    
    Args:
        query (str): Search query string
        user (User): Current authenticated user
        db (AsyncSession): Database session
    
    Returns:
        List[ContactResponse]: List of matching contacts
    """
    contact_repo = ContactRepository(db)
    contacts = await contact_repo.search_contacts(query, user.id)
    return contacts


@router.get("/birthdays/", response_model=List[ContactResponse])
async def upcoming_birthdays(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get contacts with birthdays in the next 7 days.
    
    Args:
        user (User): Current authenticated user
        db (AsyncSession): Database session
        
    Returns:
        List[ContactResponse]: List of contacts with upcoming birthdays
    """
    
    contact_repo = ContactRepository(db)
    contacts = await contact_repo.get_upcoming_birthdays(user.id)
    return contacts
