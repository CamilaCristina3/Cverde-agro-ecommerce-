from django.test import TestCase
from django.urls import reverse


class PagesViewTests(TestCase):
    """Testes para as vistas de páginas estáticas"""
    
    def test_privacy_policy_view(self):
        """Testa se a página de política de privacidade carrega"""
        response = self.client.get(reverse('pages:privacy_policy'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Pol\xc3\xadtica de Privacidade', response.content)
    
    def test_terms_of_use_view(self):
        """Testa se a página de termos de utilização carrega"""
        response = self.client.get(reverse('pages:terms_of_use'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Termos de Utiliza\xc3\xa7\xc3\xa3o', response.content)
    
    def test_cookies_policy_view(self):
        """Testa se a página de política de cookies carrega"""
        response = self.client.get(reverse('pages:cookies_policy'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Pol\xc3\xadtica de Cookies', response.content)
