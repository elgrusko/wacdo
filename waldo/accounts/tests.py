from datetime import date

from django.test import TestCase

from .forms import CollaboratorCreationForm
from .models import User


class UserModelTestCase(TestCase):
    def test_user_creation_with_custom_fields(self):
        """Checks user creation with custom fields and a hashed password."""
        user = User.objects.create_user(
            username="testuser",
            password="testpassword123",
            date_first_hired=date(2020, 1, 1),
            is_admin=True,
        )

        self.assertEqual(user.username, "testuser")
        # check_password method hashes the password and checks it against the provided string
        self.assertTrue(user.check_password("testpassword123"))
        self.assertEqual(user.date_first_hired, date(2020, 1, 1))
        self.assertTrue(user.is_admin)

    def test_user_defaults_and_string_representation(self):
        """Checks default values (is_admin/date_first_hired) and __str__."""
        user = User.objects.create_user(
            username="simpleuser",
            password="simplepassword123",
        )

        self.assertFalse(user.is_admin)
        self.assertIsNone(user.date_first_hired)
        self.assertEqual(str(user), "simpleuser")


class CollaboratorCreationFormTestCase(TestCase):
    def test_create_form_hashes_password(self):
        """Checks that a password submitted through the form is hashed on save."""
        form = CollaboratorCreationForm(
            data={
                "username": "alice",
                "first_name": "Alice",
                "last_name": "Martin",
                "email": "alice@example.com",
                "is_admin": True,
                "password": "my-safe-pass",
            }
        )

        # assertTrue(form.is_valid(), form.errors) prints form errors if the form is not valid
        self.assertTrue(form.is_valid(), form.errors)
        user = form.save()

        self.assertNotEqual(user.password, "my-safe-pass")
        self.assertTrue(user.check_password("my-safe-pass"))

    def test_edit_mode_password_optional_and_kept_if_empty(self):
        """Checks that in edit mode password is optional and blank keeps old hash."""
        user = User.objects.create_user(username="bob", password="initial-pass")
        form = CollaboratorCreationForm(
            data={
                "username": "bob",
                "first_name": "",
                "last_name": "",
                "email": "",
                "is_admin": False,
                "password": "",
            },
            instance=user,
        )

        self.assertFalse(form.fields["password"].required)
        self.assertTrue(form.is_valid(), form.errors)
        updated_user = form.save()
        self.assertTrue(updated_user.check_password("initial-pass"))
