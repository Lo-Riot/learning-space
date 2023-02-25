from django.test import TestCase
from django.core import mail
from mailings.tasks import send_verification_email


class VerificationEmailTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.email_data = {
            'from_email': "from@example.com", 'to_emails': ["to@example.com"],
            'verification_link': "https://example.com/test_verification_link"
        }

    def test_verification_email_send(self):
        send_verification_email(**self.email_data)

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(
            mail.outbox[0].from_email, self.email_data["from_email"]
        )
        self.assertEqual(mail.outbox[0].to, self.email_data["to_emails"])
