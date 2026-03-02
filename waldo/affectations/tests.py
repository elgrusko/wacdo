from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from accounts.models import User
from restaurants.models import Restaurant
from types_poste.models import TypePoste

from .forms import AffectationCreateForm, AffectationUpdateForm
from .models import Affectation


class AffectationSimpleTestCase(TestCase):
    def setUp(self):
        self.today = timezone.localdate()
        # create_user is a helper method that creates a user with the given username and password, and returns the user instance.
        self.collaborator = User.objects.create_user(
            username="alice",
            password="safe-password-123",
        )

        self.restaurant = Restaurant.objects.create(
            name="Le Central",
            address="10 Rue A",
            postal_code="75001",
            city="Paris",
        )
        self.position_type = TypePoste.objects.create(label="Serveur")

    def test_affectation_string_representation(self):
        """Checks Affectation.__str__ format."""
        affectation = Affectation.objects.create(
            collaborator=self.collaborator,
            restaurant=self.restaurant,
            position_type=self.position_type,
            start_date=self.today,
        )

        expected = f"{self.collaborator} -> {self.restaurant} ({self.position_type})"
        self.assertEqual(str(affectation), expected)

    def test_create_form_valid_data(self):
        """Checks create form is valid with correct data and restaurant context."""
        form = AffectationCreateForm(
            data={
                "collaborator": self.collaborator.id,
                "position_type": self.position_type.id,
                "start_date": self.today.isoformat(),
                "end_date": "",
            },
            restaurant=self.restaurant,
        )

        self.assertTrue(form.is_valid(), form.errors)
        affectation = form.save()
        self.assertEqual(affectation.restaurant, self.restaurant)

    def test_create_form_rejects_end_date_before_start_date(self):
        """Checks create form rejects end_date earlier than start_date."""
        form = AffectationCreateForm(
            data={
                "collaborator": self.collaborator.id,
                "position_type": self.position_type.id,
                "start_date": self.today.isoformat(),
                # end_date before start_date should trigger a validation error
                "end_date": (self.today - timedelta(days=1)).isoformat(),
            },
            restaurant=self.restaurant,
        )

        self.assertFalse(form.is_valid())
        self.assertIn("__all__", form.errors)

    def test_create_form_save_requires_restaurant_context(self):
        """Checks create form save raises if restaurant context is missing."""
        form = AffectationCreateForm(
            data={
                "collaborator": self.collaborator.id,
                "position_type": self.position_type.id,
                "start_date": self.today.isoformat(),
                "end_date": "",
            }
        )
        # Voluntarily not providing the restaurant context 
        # restaurant=self.restaurant

        self.assertTrue(form.is_valid(), form.errors)
        with self.assertRaisesMessage(ValueError, "Restaurant manquant"):
            form.save()

    def test_update_form_requires_end_date(self):
        """Checks update form requires end_date."""
        affectation = Affectation.objects.create(
            collaborator=self.collaborator,
            restaurant=self.restaurant,
            position_type=self.position_type,
            start_date=self.today,
            #end_date is null, which should be invalid for the update form since end_date is required in update mode
        )
        form = AffectationUpdateForm(data={"end_date": ""}, instance=affectation)

        self.assertFalse(form.is_valid())
        self.assertIn("end_date", form.errors)
