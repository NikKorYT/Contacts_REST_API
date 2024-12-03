from fastapi import APIRouter, Query, Path

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
@router.get("/contact/{contact_id}")
async def get_contact(
    contact_id: int = Path(
        description="The ID of the contact you want to retrieve", gt=0, le=10
    )
):
    return {"contact_id": contact_id}
