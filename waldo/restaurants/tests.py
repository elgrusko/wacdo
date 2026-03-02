from django.test import TestCase

from .forms import RestaurantForm, RestaurantSearchForm
from .models import Restaurant


class RestaurantModelTestCase(TestCase):
    def test_restaurant_string_representation(self):
        """Checks that __str__ returns 'name - city'."""
        restaurant = Restaurant.objects.create(
            name="Le Bistrot",
            address="12 Rue de Paris",
            postal_code="75001",
            city="Paris",
        )

        self.assertEqual(str(restaurant), "Le Bistrot - Paris")


class RestaurantFormTestCase(TestCase):
    def test_restaurant_form_valid_data(self):
        """Checks that RestaurantForm is valid with required fields."""
        form = RestaurantForm(
            data={
                "name": "Chez Anna",
                "address": "3 Avenue Centrale",
                "postal_code": "69001",
                "city": "Lyon",
            }
        )

        self.assertTrue(form.is_valid(), form.errors)
        restaurant = form.save()
        self.assertEqual(restaurant.name, "Chez Anna")
        self.assertEqual(restaurant.city, "Lyon")

    def test_restaurant_form_requires_city(self):
        """Checks that city is required in RestaurantForm."""
        form = RestaurantForm(
            data={
                "name": "Chez Anna",
                "address": "3 Avenue Centrale",
                "postal_code": "69001",
                "city": "",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("city", form.errors)


class RestaurantSearchFormTestCase(TestCase):
    def test_search_form_is_valid_with_empty_data(self):
        """Checks that search form is valid when all filters are empty."""
        form = RestaurantSearchForm(data={})

        self.assertTrue(form.is_valid(), form.errors)
