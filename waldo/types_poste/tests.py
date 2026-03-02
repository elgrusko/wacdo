from django.test import TestCase

from .forms import TypePosteForm
from .models import TypePoste


class TypePosteFormTestCase(TestCase):
    def test_label_is_cleaned_with_strip_and_title(self):
        """Checks that the form normalizes label (trim + title case)."""
        form = TypePosteForm(data={"label": "   chef de rang   "})

        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.cleaned_data["label"], "Chef De Rang")

        poste = form.save()
        self.assertEqual(poste.label, "Chef De Rang")

    def test_duplicate_label_is_rejected_after_normalization(self):
        """Checks that duplicates are rejected even with case/space differences."""
        TypePoste.objects.create(label="Serveur")

        form = TypePosteForm(data={"label": "   serveur   "})

        self.assertFalse(form.is_valid())
        self.assertIn("label", form.errors)

    def test_label_is_required(self):
        """Checks that label is required (form invalid when empty)."""
        form = TypePosteForm(data={"label": ""})

        self.assertFalse(form.is_valid())
        self.assertIn("label", form.errors)
