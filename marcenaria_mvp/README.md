# Marcenaria MVP

Sistema de gestão simplificado para marceneiros autônomos e pequenas marcenarias.

## 🛠️ Tech Stack

- **Backend:** Django 5.x + Python 3.12
- **Frontend:** HTML5 + CSS3 + Bootstrap 5.3
- **Database:** SQLite
- **Storage:** AWS S3 (Configurado via `boto3`)
- **Integrações:** WhatsApp Business API, WeasyPrint (PDFs)

## 🚀 Como Iniciar o Projeto

### 1. Pré-requisitos

Certifique-se de ter o Python 3.12+ instalado.

### 2. Configuração do Ambiente

```bash
# Clone o repositório (se aplicável) ou navegue até a pasta do projeto
cd marcenaria_mvp

# Crie um ambiente virtual
python -m venv .venv

# Ative o ambiente virtual
# Windows (PowerShell):
.\.venv\Scripts\Activate
# Linux/Mac:
source .venv/bin/activate

# Instale as dependências
pip install django weasyprint boto3 requests pillow
```

### 3. Configuração do Banco de Dados

```bash
# Crie as migrações iniciais
python manage.py makemigrations

# Aplique as migrações ao banco de dados
python manage.py migrate

# Crie um superusuário para acessar o admin
python manage.py createsuperuser
```

### 4. Executando o Servidor

```bash
python manage.py runserver
```

Acesse o sistema em: `http://127.0.0.1:8000/`

## 📂 Estrutura do Projeto

```
marcenaria_mvp/
├── core/                   # App principal
│   ├── models.py           # Modelos (Cliente, Orcamento)
│   ├── views.py            # Lógica das views
│   ├── forms.py            # Formulários Django
│   └── templates/          # Templates HTML (Bootstrap 5)
├── marcenaria/             # Configurações do projeto
│   ├── settings.py         # Configurações globais (S3, WhatsApp)
│   └── urls.py             # Rotas principais
├── static/                 # Arquivos estáticos (CSS, JS)
├── media/                  # Uploads de usuários
└── manage.py               # Utilitário de comando Django
```

## ✅ Funcionalidades Implementadas

- [x] Autenticação (Login/Logout)
- [x] Dashboard com métricas iniciais
- [x] CRUD de Clientes (Listar, Criar, Buscar)
- [x] Design System com Bootstrap 5 e cores personalizadas
- [ ] CRUD de Orçamentos (Em breve)
- [ ] Geração de PDF e Envio WhatsApp (Em breve)

## ⚠️ Notas Importantes

- **Ambiente Virtual:** Sempre ative o ambiente virtual (`.venv`) antes de rodar comandos do Django. Se receber erro de `ImportError`, verifique se o venv está ativo.
- **Configurações:** As chaves de API (AWS, WhatsApp) devem ser configuradas no arquivo `marcenaria/settings.py` antes de usar essas funcionalidades em produção.
