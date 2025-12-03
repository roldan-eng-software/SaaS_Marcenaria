# DIRETRIZ DO PROJETO

## 🎯 CONTEXTO DO PROJETO
Crie um MVP completo de software de gestão para marceneiros autônomos usando **apenas Django + HTML/CSS/Bootstrap5 + SQLite**.

**Público:** Marceneiros autônomos e pequenas marcenarias
**Ticket:** R$149/mês com InfinitePay
**Core features:** Orçamentos, Clientes, WhatsApp, Imagens S3

## 🛠️ STACK EXATA (NÃO MUDA)
BACKEND: Django 5.x + Python 3.12
FRONTEND: HTML + CSS + Bootstrap 5.3 (SEM React/Vue/Alpine)
DATABASE: SQLite (models.py + migrations)
ARQUIVOS: AWS S3 (boto3)
WHATSAPP: API Oficial (requests)
PAGAMENTO: InfinitePay (webhooks)

text

## 📋 FUNCIONALIDADES MVP (EXATAMENTE ESTAS)

### 1. AUTENTICAÇÃO
Login/register admin (Django Auth)

Dashboard inicial /admin/

Logout funcional

text

### 2. CRUD CLIENTES
Model: Cliente

nome (CharField)

whatsapp (+5511999999999 format)

email, telefone, endereco

created_at

Tabelas Bootstrap responsiva

Busca/filtro por nome

text

### 3. CRUD ORÇAMENTOS (CORE)
Model: Orcamento

cliente (ForeignKey)

data_criacao (DateTimeField)

itens (JSONField): [{"material": "MDF 15mm", "qtd": 2, "preco_unit": 150.00}]

total (DecimalField)

status: ['rascunho', 'enviado', 'aprovado']

imagens (JSONField): [{"s3_url": " `https://...` ", "descricao": "Frente"}]

Views:

/orcamentos/novo/ → Form criar

/orcamentos/[id]/editar/ → Editar

/orcamentos/[id]/enviar/ → Gerar PDF + WhatsApp

/orcamentos/ → Lista com filtros (status, data)

text

### 4. UPLOAD IMAGENS S3
Múltiplo upload no form orçamento

Salvar URLs no JSONField

Preview thumbnails Bootstrap

boto3 configurado (settings.py)

text

### 5. ENVIO WHATSAPP
Botão "Enviar WhatsApp"

Gerar PDF orçamento (WeasyPrint)

POST para WhatsApp Business API

Template mensagem: "Olá {nome}! Seu orçamento: [PDF]"

text

## 🎨 DESIGN SYSTEM (OBRIGATÓRIO)

**Cores:**
--verde-madeira: #2C5530
--dourado-ferramenta: #D4A017
--marrom: #8B4513
--bg: #F8F9FA

text

**Páginas (Bootstrap cards + tables):**
/ → Login

/dashboard/ → Cards: orçamentos pendentes, clientes novos, receita

/clientes/ → Tabela Bootstrap + search

/orcamentos/novo/ → Form stepwise (cliente → itens → imagens)

/orcamentos/[id]/ → Detalhes + ações (editar/enviar)

text

## 🗄️ MODELOS DJANGO EXATOS

models.py
class Cliente(models.Model):
nome = models.CharField(max_length=100)
whatsapp = models.CharField(max_length=15, unique=True)
email = models.EmailField(blank=True)
endereco = models.TextField(blank=True)
created_at = models.DateTimeField(auto_now_add=True)

class Orcamento(models.Model):
STATUS = [
('rascunho', 'Rascunho'),
('enviado', 'Enviado'),
('aprovado', 'Aprovado')
]

text
cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
data_criacao = models.DateTimeField(auto_now_add=True)
itens = models.JSONField(default=list)  # [{"material": "...", "qtd": 2, "preco_unit": 150}]
total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
status = models.CharField(max_length=10, choices=STATUS, default='rascunho')
imagens = models.JSONField(default=list)  # [{"s3_url": "...", "descricao": "..."}]
text

## 📂 ESTRUTURA PROJETO FINAL
marcenaria_mvp/
├── manage.py
├── marcenaria/
│ ├── settings.py (S3, WhatsApp API keys)
│ ├── urls.py
│ └── wsgi.py
├── core/
│ ├── models.py
│ ├── views.py
│ ├── forms.py
│ ├── urls.py
│ └── templates/
│ ├── base.html (Bootstrap5)
│ ├── dashboard.html
│ ├── clientes_list.html
│ └── orcamentos_form.html
└── static/
├── css/custom.css
└── js/orcamento.js (vanilla)

text

## 🚀 COMANDOS INICIAIS
django-admin startproject marcenaria_mvp
cd marcenaria_mvp
python manage.py startapp core
pip install django weasyprint boto3 requests pillow
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver

text

## 🎯 PRIMEIRO CHECKPOINT (24h)
✅ [ ] Django rodando localhost:8000
✅ [ ] Login/register funcionando
✅ [ ] CRUD clientes (listar + novo)
✅ [ ] Bootstrap5 aplicado
✅ [ ] Models Orcamento criados

text

## ⚠️ REGRAS RÍGIDAS PARA O CURSOR
1. **NUNCA** usar React/Vue/Alpine/Tailwind
2. **APENAS** Bootstrap5 + vanilla JS
3. **SEM** DRF/serializers (views class-based simples)
4. **TODO** em HTML forms + CSRF
5. **CÓDIGO LIMPO** Django vanilla (sem pacotes obscuros)

## 📋 TAREFAS PRIORITÁRIAS (COMECE POR ESTA ORDEM)
Criar projeto Django + app 'core'

Models Cliente + Orcamento + migrations

Login/register views + templates Bootstrap

CRUD clientes completo

Dashboard inicial com cards Bootstrap

Form orçamento novo (sem JS ainda)

text

**COMECE AGORA! Gere a estrutura inicial + login + models. Depois CRUD clientes.**

**META SEMANA 1:** CRUD clientes + dashboard funcionando perfeitamente.

