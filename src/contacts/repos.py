from sqlalchemy import select

from src.contacts.models import Contact

class ContactRepository:
    
    
    def __init__(self, session):
        self.db = session
        
    async def get_contacts(self, contact_id: int) -> Contact:
        
        query = self.db.query(Contact).where(Contact.id == contact_id)
        result = await self.session.execute(query)
        
        return result.scalar.one_or_none()