import unittest
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import date, datetime, timedelta
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
    _id = MagicMock()
    owner_id = MagicMock()
    name = MagicMock()
    surname = MagicMock()
    email = MagicMock()
    date_of_birth = MagicMock()

    name.ilike = MagicMock(return_value=True)
    surname.ilike = MagicMock(return_value=True)
    email.ilike = MagicMock(return_value=True)

    def __init__(self, **kwargs):
        self._instance_id = kwargs.get("id")
        self.name = kwargs.get("name")
        self.surname = kwargs.get("surname")
        self.email = kwargs.get("email")
        self.phone = kwargs.get("phone")
        self.date_of_birth = kwargs.get("date_of_birth")
        self.owner_id = kwargs.get("owner_id")
        self.owner = MockUser(id=self.owner_id) if self.owner_id else None

    @property
    def id(self):
        return self._instance_id if hasattr(self, "_instance_id") else self._id


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
        
    async def test_delete_contact(self):
        # Arrange
        contact_id = 1
        mock_contact = MockContact(
            id=contact_id,
            name="Test",
            surname="User",
            email="test@test.com",
            phone=1234567890,
            date_of_birth=date(1990, 1, 1),
            owner_id=self.user_id
        )
        
        # Mock get_contacts to return our mock contact
        self.repo.get_contacts = AsyncMock(return_value=mock_contact)

        # Act
        result = await self.repo.delete_contact(contact_id)

        # Assert
        self.repo.get_contacts.assert_awaited_once_with(contact_id)
        self.session.delete.assert_called_once_with(mock_contact)
        self.session.commit.assert_awaited_once()
        self.assertEqual(result, mock_contact)
    async def test_contact_update_success(self):
        # Arrange
        contact_id = 1
        updated_data = MockContactCreate(
            name="Updated",
            surname="User",
            email="updated@test.com",
            phone=9876543210,
            date_of_birth=date(1990, 1, 1),
        )

        mock_contact = MockContact(
            id=contact_id,
            name="Original",
            surname="User",
            email="test@test.com",
            phone=1234567890,
            date_of_birth=date(1990, 1, 1),
            owner_id=self.user_id,
        )

        # Setup mock execution result
        mock_result = MagicMock()
        mock_result.scalar_one_or_none = MagicMock(return_value=mock_contact)
        self.session.execute.return_value = mock_result

        # Act
        result = await self.repo.contact_update(contact_id, updated_data)

        # Assert
        self.assertEqual(result.name, updated_data.name)
        self.assertEqual(result.email, updated_data.email)
        self.session.commit.assert_awaited_once()
        self.session.refresh.assert_awaited_once_with(result)

    async def test_contact_update_not_found(self):
        # Arrange
        contact_id = 999
        updated_data = MockContactCreate(
            name="Updated",
            surname="User",
            email="updated@test.com",
            phone=9876543210,
            date_of_birth=date(1990, 1, 1),
        )

        # Setup mock execution result for non-existent contact
        mock_result = MagicMock()
        mock_result.scalar_one_or_none = MagicMock(return_value=None)
        self.session.execute.return_value = mock_result

        # Act
        result = await self.repo.contact_update(contact_id, updated_data)

        # Assert
        self.assertIsNone(result)
        self.session.commit.assert_not_awaited()
        self.session.refresh.assert_not_awaited()
        
    async def test_get_all_contacts_default_pagination(self):
        # Arrange
        mock_contacts = [
            MockContact(
                id=1,
                name="Test1",
                surname="User1",
                email="test1@test.com",
                phone=1234567890,
                date_of_birth=date(1990, 1, 1),
                owner_id=self.user_id
            ),
            MockContact(
                id=2,
                name="Test2",
                surname="User2",
                email="test2@test.com",
                phone=9876543210,
                date_of_birth=date(1990, 1, 1),
                owner_id=self.user_id
            )
        ]
        
        # Setup mock execution result
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = mock_contacts
        self.session.execute.return_value = mock_result

        # Act
        result = await self.repo.get_all_contacts(self.user_id)

        # Assert
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].name, "Test1")
        self.assertEqual(result[1].name, "Test2")
        self.session.execute.assert_called_once()

    async def test_get_all_contacts_custom_pagination(self):
        # Arrange
        skip = 2
        limit = 2
        mock_contacts = [
            MockContact(
                id=3,
                name="Test3",
                surname="User3",
                email="test3@test.com",
                phone=1234567890,
                date_of_birth=date(1990, 1, 1),
                owner_id=self.user_id
            )
        ]
        
        # Setup mock execution result
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = mock_contacts
        self.session.execute.return_value = mock_result

        # Act
        result = await self.repo.get_all_contacts(self.user_id, skip=skip, limit=limit)

        # Assert
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].name, "Test3")
        self.session.execute.assert_called_once()
        
    async def test_search_contacts_with_matches(self):
        # Arrange
        search_text = "test"
        mock_contacts = [
            MockContact(
                id=1,
                name="Test User",
                surname="Smith",
                email="test@test.com",
                phone=1234567890,
                date_of_birth=date(1990, 1, 1),
                owner_id=self.user_id
            ),
            MockContact(
                id=2,
                name="John",
                surname="Test",
                email="john@test.com",
                phone=9876543210,
                date_of_birth=date(1990, 1, 1),
                owner_id=self.user_id
            )
        ]
        
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = mock_contacts
        self.session.execute.return_value = mock_result

        # Act
        result = await self.repo.search_contacts(search_text, self.user_id)

        # Assert
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].name, "Test User")
        self.assertEqual(result[1].surname, "Test")
        self.session.execute.assert_called_once()

    async def test_search_contacts_no_matches(self):
        # Arrange
        search_text = "nonexistent"
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = []
        self.session.execute.return_value = mock_result

        # Act
        result = await self.repo.search_contacts(search_text, self.user_id)

        # Assert
        self.assertEqual(len(result), 0)
        self.session.execute.assert_called_once()
    
    async def test_get_upcoming_birthdays_with_matches(self):
        # Arrange
        today = datetime.now().date()
        mock_contacts = [
            MockContact(
                id=1,
                name="Birthday Today",
                surname="User1",
                email="today@test.com",
                phone=1234567890,
                date_of_birth=date(1990, today.month, today.day),
                owner_id=self.user_id
            ),
            MockContact(
                id=2,
                name="Birthday Next Week",
                surname="User2",
                email="nextweek@test.com",
                phone=9876543210,
                date_of_birth=date(1990, today.month, today.day + 5),
                owner_id=self.user_id
            )
        ]
        
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = mock_contacts
        self.session.execute.return_value = mock_result

        # Act
        result = await self.repo.get_upcoming_birthdays(self.user_id)

        # Assert
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].name, "Birthday Today")
        self.assertEqual(result[1].name, "Birthday Next Week")
        self.session.execute.assert_called_once()

    async def test_get_upcoming_birthdays_no_matches(self):
        # Arrange
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = []
        self.session.execute.return_value = mock_result

        # Act
        result = await self.repo.get_upcoming_birthdays(self.user_id)

        # Assert
        self.assertEqual(len(result), 0)
        self.session.execute.assert_called_once()

    async def test_get_upcoming_birthdays_cross_month(self):
        # Arrange
        today = datetime.now().date()
        next_month = today.replace(day=1) + timedelta(days=32)
        mock_contacts = [
            MockContact(
                id=1,
                name="Cross Month Birthday",
                surname="User",
                email="crossmonth@test.com",
                phone=1234567890,
                date_of_birth=date(1990, next_month.month, 1),
                owner_id=self.user_id
            )
        ]
        
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = mock_contacts
        self.session.execute.return_value = mock_result

        # Act
        result = await self.repo.get_upcoming_birthdays(self.user_id)

        # Assert
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].name, "Cross Month Birthday")
        self.session.execute.assert_called_once()
    
    async def test_get_contacts_found(self):
        # Arrange
        contact_id = 1
        mock_contact = MockContact(
            id=contact_id,
            name="Test",
            surname="User",
            email="test@test.com",
            phone=1234567890,
            date_of_birth=date(1990, 1, 1),
            owner_id=self.user_id
        )
        
        # Setup mock execution result
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_contact
        self.session.execute.return_value = mock_result

        # Act
        result = await self.repo.get_contacts(contact_id)

        # Assert
        self.assertEqual(result.id, contact_id)
        self.assertEqual(result.name, "Test")
        self.assertEqual(result.email, "test@test.com")
        self.session.execute.assert_called_once()

    async def test_get_contacts_not_found(self):
        # Arrange
        contact_id = 999
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        self.session.execute.return_value = mock_result

        # Act
        result = await self.repo.get_contacts(contact_id)

        # Assert
        self.assertIsNone(result)
        self.session.execute.assert_called_once()

if __name__ == "__main__":
    unittest.main()
