from django.test import SimpleTestCase, override_settings
from django.urls import reverse

GIFT_ACCOUNTS = [
    {
        'flag': '🇪🇺',
        'country': 'Europe',
        'details': [('IBAN', 'XX99 SECRET 1234')],
    },
]


@override_settings(ALLOWED_HOSTS=['*'], GIFT_ACCOUNTS=GIFT_ACCOUNTS)
class GiftAccountsTest(SimpleTestCase):

    def test_homepage_masks_account_details(self):
        response = self.client.get(reverse('home'))
        self.assertContains(response, 'IBAN')
        self.assertContains(response, reverse('gift-account', args=[0]))
        self.assertNotContains(response, 'XX99 SECRET 1234')

    def test_gift_account_endpoint_returns_values(self):
        response = self.client.get(reverse('gift-account', args=[0]))
        self.assertEqual(response.json(), {'values': ['XX99 SECRET 1234']})
        self.assertEqual(response['X-Robots-Tag'], 'noindex, nofollow')
        self.assertIn('no-cache', response['Cache-Control'])

    def test_unknown_gift_account_is_404(self):
        response = self.client.get(reverse('gift-account', args=[5]))
        self.assertEqual(response.status_code, 404)
