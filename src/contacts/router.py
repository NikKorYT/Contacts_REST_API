from fastapi import APIRouter, Query, Path

from src.contacts.schemas import Contact, ContactResponse

router = APIRouter()

@router.post("/contact")
async def create_contact(contact: Contact) -> ContactResponse:
    return ContactResponse(first_name=contact.name, last_name=contact.surname)


@router.get("/contact/{contact_id}")
async def get_contact(
    contact_id: int = Path(
        description="The ID of the contact you want to retrieve", gt=0, le=10
    )
):
    return {"contact_id": contact_id}
