# software/tests.py
from django.test import TestCase
from .models import NewsletterSubscriber # Import your model if you want to test it

class NewsletterSubscriberModelTest(TestCase):
    def test_subscriber_creation(self):
        """
        Tests that a NewsletterSubscriber can be created.
        """
        subscriber = NewsletterSubscriber.objects.create(email='test@example.com')
        self.assertEqual(subscriber.email, 'test@example.com')
        self.assertIsNotNone(subscriber.pk)

    def test_unique_email(self):
        """
        Tests that duplicate emails cannot be created.
        """
        NewsletterSubscriber.objects.create(email='unique@example.com')
        with self.assertRaises(Exception): # Will catch IntegrityError or ValidationError depending on Django version
            NewsletterSubscriber.objects.create(email='unique@example.com')

# You can add more test classes/functions here
class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)