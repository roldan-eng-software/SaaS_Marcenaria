from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Cliente, Orcamento
from .forms import OrcamentoForm

class ModelTests(TestCase):
    def test_cliente_str(self):
        cliente = Cliente.objects.create(nome='João', whatsapp='11999999999')
        self.assertEqual(str(cliente), 'João')

    def test_orcamento_str(self):
        cliente = Cliente.objects.create(nome='Maria', whatsapp='11988888888')
        orcamento = Orcamento.objects.create(cliente=cliente, total=100)
        self.assertIn('Orçamento #', str(orcamento))
        self.assertIn('Maria', str(orcamento))

class FormTests(TestCase):
    def test_orcamento_form_clean_itens_valid_json(self):
        data = {
            'cliente': Cliente.objects.create(nome='Ana', whatsapp='11977777777').id,
            'status': 'rascunho',
            'itens': '[{"material":"Madeira","qtd":2,"preco_unit":50}]',
            'imagens': '[]',
            'total': 100,
        }
        form = OrcamentoForm(data)
        self.assertTrue(form.is_valid())
        self.assertEqual(len(form.cleaned_data['itens']), 1)

    def test_orcamento_form_clean_itens_invalid_json(self):
        data = {
            'cliente': Cliente.objects.create(nome='Pedro', whatsapp='11966666666').id,
            'status': 'rascunho',
            'itens': '[invalid',
            'imagens': '[]',
            'total': 0,
        }
        form = OrcamentoForm(data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['itens'], [])

class ViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user', password='pass')
        self.client.login(username='user', password='pass')

    def test_dashboard_view(self):
        url = reverse('dashboard')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_clientes_list_search(self):
        Cliente.objects.create(nome='Carlos', whatsapp='11955555555')
        Cliente.objects.create(nome='Carla', whatsapp='11944444444')
        url = reverse('clientes_list')
        resp = self.client.get(url, {'q': 'Carl'})
        self.assertEqual(resp.status_code, 200)
