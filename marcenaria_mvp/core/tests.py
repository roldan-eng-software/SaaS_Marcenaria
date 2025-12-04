from django.test import TestCase
from django.contrib.auth.models import User
from .models import Cliente, Orcamento, ItemOrcamento, ImagemOrcamento
from django.urls import reverse

class CoreTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')

    def test_cliente_creation(self):
        """Test the creation of a cliente"""
        cliente = Cliente.objects.create(
            user=self.user,
            nome='Test Cliente',
            whatsapp='123456789',
            email='test@test.com',
            endereco='Test Address'
        )
        self.assertEqual(cliente.nome, 'Test Cliente')
        self.assertEqual(cliente.user, self.user)

    def test_orcamento_creation(self):
        """Test the creation of an orcamento"""
        cliente = Cliente.objects.create(
            user=self.user,
            nome='Test Cliente',
            whatsapp='123456789',
            email='test@test.com',
            endereco='Test Address'
        )
        orcamento = Orcamento.objects.create(
            user=self.user,
            cliente=cliente,
            total=100.00
        )
        self.assertEqual(orcamento.total, 100.00)
        self.assertEqual(orcamento.user, self.user)
        self.assertEqual(orcamento.cliente, cliente)

    def test_cliente_list_view(self):
        """Test the cliente list view"""
        response = self.client.get(reverse('clientes_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'clientes_list.html')

    def test_cliente_create_view(self):
        """Test the cliente create view"""
        response = self.client.post(reverse('cliente_create'), {
            'nome': 'New Cliente',
            'whatsapp': '987654321',
            'email': 'new@test.com',
            'endereco': 'New Address'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Cliente.objects.filter(nome='New Cliente').exists())

    def test_orcamento_list_view(self):
        """Test the orcamento list view"""
        response = self.client.get(reverse('orcamento_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'orcamento_list.html')

    def test_orcamento_create_view(self):
        """Test the orcamento create view"""
        cliente = Cliente.objects.create(
            user=self.user,
            nome='Test Cliente',
            whatsapp='123456789',
            email='test@test.com',
            endereco='Test Address'
        )
        response = self.client.post(reverse('orcamento_create'), {
            'cliente': cliente.id,
            'status': 'rascunho',
            'total': 200.00,
            'itens-TOTAL_FORMS': '1',
            'itens-INITIAL_FORMS': '0',
            'itens-MIN_NUM_FORMS': '0',
            'itens-MAX_NUM_FORMS': '1000',
            'itens-0-material': 'Test Material',
            'itens-0-quantidade': '2',
            'itens-0-preco_unitario': '100.00',
            'imagens-TOTAL_FORMS': '0',
            'imagens-INITIAL_FORMS': '0',
            'imagens-MIN_NUM_FORMS': '0',
            'imagens-MAX_NUM_FORMS': '1000',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Orcamento.objects.filter(total=200.00).exists())
