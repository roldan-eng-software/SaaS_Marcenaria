# 🪵 Marcenaria Pro - Sistema de Gestão para Marceneiros

Sistema completo de gestão para marceneiros autônomos e pequenas marcenarias, desenvolvido com Django.

## 🎯 Funcionalidades

### ✅ Gestão de Clientes
- Cadastro completo (nome, WhatsApp, email, endereço)
- Busca por nome
- Edição de dados

### 📋 Gestão de Orçamentos
- Criação de orçamentos com múltiplos itens
- Cálculo automático de totais
- Upload de imagens de referência (DigitalOcean Spaces)
- Geração de PDF profissional
- Envio automático via WhatsApp
- Controle de status (Rascunho, Enviado, Aprovado)
- Filtros por status e data

### 📊 Dashboard
- Visão geral de orçamentos pendentes
- Total de clientes
- Receita de orçamentos aprovados

## 🛠️ Tecnologias

- **Backend:** Django 5.x + Python 3.12
- **Frontend:** HTML + CSS + Bootstrap 5.3
- **Banco de Dados:** SQLite (dev) / PostgreSQL (prod)
- **Armazenamento:** DigitalOcean Spaces (S3-compatible)
- **PDF:** WeasyPrint
- **Mensagens:** WhatsApp Business API

## 🚀 Quick Start

### 1. Clone e Configure
```bash
cd marcenaria_mvp
python -m venv .venv
.venv\Scripts\Activate.ps1  # Windows
pip install -r requirements.txt
```

### 2. Configure Variáveis de Ambiente
```bash
cp .env.example .env
# Edite .env com suas credenciais
```

### 3. Inicialize o Banco
```bash
python manage.py migrate
python manage.py createsuperuser
```

### 4. Execute
```bash
python manage.py runserver
```

Acesse: `http://localhost:8000`

## 📖 Documentação Completa

- [Guia de Deploy](DEPLOY.md) - Instruções detalhadas para produção
- [DIRETRIZ.md](../DIRETRIZ.md) - Especificações do projeto

## 🎨 Design System

```css
--verde-madeira: #2C5530
--dourado-ferramenta: #D4A017
--marrom: #8B4513
--bg: #F8F9FA
```

## 📁 Estrutura do Projeto

```
marcenaria_mvp/
├── core/                   # App principal
│   ├── models.py          # Cliente, Orcamento
│   ├── views.py           # Lógica de negócio
│   ├── forms.py           # Formulários
│   ├── templates/         # Templates HTML
│   └── templatetags/      # Filtros customizados
├── marcenaria/            # Configurações Django
│   └── settings.py        # Configurações + env vars
├── static/                # Arquivos estáticos
├── .env.example           # Template de variáveis
└── requirements.txt       # Dependências Python
```

## 🔐 Segurança

- Autenticação obrigatória para todas as views
- CSRF protection habilitado
- Variáveis sensíveis em `.env`
- HTTPS em produção (recomendado)

## 📝 Licença

Projeto desenvolvido para uso comercial.

## 🤝 Contribuindo

Este é um projeto privado. Para sugestões ou melhorias, entre em contato.

---

**Desenvolvido com ❤️ para marceneiros profissionais**
