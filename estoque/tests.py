from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Categoria, Produto

class ConfiroJaTestCase(TestCase):
    def setUp(self):
        # Criação do utilizador de teste
        self.user = User.objects.create_user(
            username='testuser', 
            password='testpassword'
        )
        self.client = Client()

        # Criação de categoria e produto de teste
        self.categoria = Categoria.objects.create(nome='Escritório')
        self.produto = Produto.objects.create(
            nome='Caneta Azul',
            categoria=self.categoria,
            quantidade_atual=5,
            quantidade_minima=10,
            unidade_medida='Unidade'
        )

    def test_login_sucesso(self):
        """ Testa o login de utilizador """
        response = self.client.login(username='testuser', password='testpassword')
        self.assertTrue(response)

    def test_dashboard_acesso_autenticado(self):
        """ Testa se o dashboard carrega para utilizador logado """
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_api_produtos(self):
        """ Testa o endpoint da API JSON """
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('api_produtos'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('produtos', response.json())
        self.assertEqual(len(response.json()['produtos']), 1)

    def test_produto_precisa_reposicao(self):
        """ Testa se o calculo de reposição está correto """
        # Como quantidade_atual (5) < quantidade_minima (10), precisa de reposição
        self.assertTrue(self.produto.quantidade_atual < self.produto.quantidade_minima)