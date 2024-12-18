import unittest
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession


# Simple mock classes without SQLAlchemy dependencies
class MockUser:
    def __init__(self, id=1):
        self.id = id
        self.email = "test@test.com"
        self.username = "testuser"


class MockContactCreate:
    def __init__(self, **kwargs):
        self.name = kwargs.get("name")
        self.surname = kwargs.get("surname")
        self.email = kwargs.get("email")
        self.phone = kwargs.get("phone")
        self.date_of_birth = kwargs.get("date_of_birth")

    def model_dump(self):
        return {
            "name": self.name,
            "surname": self.surname,
            "email": self.email,
            "phone": self.phone,
            "date_of_birth": self.date_of_birth,
        }


class MockContact:
    @property
    def id(self):
        return MagicMock()

    def __init__(self, **kwargs):
        self._id = kwargs.get("id", 1)
        self.name = kwargs.get("name")
        self.surname = kwargs.get("surname")
        self.email = kwargs.get("email")
        self.phone = kwargs.get("phone")
        self.date_of_birth = kwargs.get("date_of_birth")
        self.owner_id = kwargs.get("owner_id")
        self.owner = MockUser(id=self.owner_id) if self.owner_id else None

    @classmethod
    def id(cls):
        return MagicMock()


# Mock select() before importing repository
with patch("sqlalchemy.select") as mock_select:
    with patch("src.auth.models.User", MockUser):
        with patch("src.contacts.models.Contact", MockContact):
            from src.contacts.repos import ContactRepository


@patch("src.auth.models.User", MockUser)
@patch("src.contacts.models.Contact", MockContact)
class TestContactRepository(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.session = AsyncMock(spec=AsyncSession)
        self.user_id = 1
        self.repo = ContactRepository(self.session)

    async def test_create_contact(self):
        # Arrange
        contact_data = MockContactCreate(
            name="Test",
            surname="User",
            email="test@test.com",
            phone=1234567890,
            date_of_birth=date(1990, 1, 1),
        )

        # Act
        result = await self.repo.create_contact(contact_data, self.user_id)

        # Assert
        self.assertEqual(result.name, contact_data.name)
        self.assertEqual(result.owner_id, self.user_id)
        self.session.add.assert_called_once()
        self.session.commit.assert_awaited_once()
        self.session.refresh.assert_awaited_once()


if __name__ == "__main__":
    unittest.main()
