# Guia de Deploy - Marcenaria MVP

## 📋 Pré-requisitos

- Python 3.12+
- Git
- Conta DigitalOcean Spaces (para armazenamento de imagens)
- Conta WhatsApp Business API (para envio de mensagens)

---

## 🚀 Deploy Local (Desenvolvimento)

### 1. Clone o Repositório
```bash
cd marcenaria_mvp
```

### 2. Crie o Ambiente Virtual
```bash
python -m venv .venv
```

### 3. Ative o Ambiente Virtual

**Windows (PowerShell):**
```powershell
.venv\Scripts\Activate.ps1
```

**Windows (CMD):**
```cmd
.venv\Scripts\activate.bat
```

**Linux/Mac:**
```bash
source .venv/bin/activate
```

### 4. Instale as Dependências
```bash
pip install -r requirements.txt
```

### 5. Configure as Variáveis de Ambiente

Copie o arquivo `.env.example` para `.env`:
```bash
cp .env.example .env
```

Edite o arquivo `.env` com suas credenciais:
```env
# Django
SECRET_KEY=sua-chave-secreta-aqui
DEBUG=True

# DigitalOcean Spaces
AWS_ACCESS_KEY_ID=sua-access-key
AWS_SECRET_ACCESS_KEY=sua-secret-key
AWS_STORAGE_BUCKET_NAME=seu-bucket-name
AWS_S3_REGION_NAME=nyc3
AWS_S3_ENDPOINT_URL=https://nyc3.digitaloceanspaces.com

# WhatsApp API
WHATSAPP_API_TOKEN=seu-token-whatsapp
WHATSAPP_PHONE_NUMBER_ID=seu-phone-id
```

### 6. Execute as Migrações
```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Crie um Superusuário
```bash
python manage.py createsuperuser
```

### 8. Inicie o Servidor
```bash
python manage.py runserver
```

Acesse: `http://localhost:8000`

---

## 🌐 Deploy em Produção

### Opção 1: DigitalOcean App Platform (Recomendado)

#### 1. Prepare o Projeto

Crie `runtime.txt` na raiz:
```
python-3.12.0
```

Atualize `settings.py` para produção:
```python
# Adicione ao final do settings.py
import os

if not DEBUG:
    ALLOWED_HOSTS = [os.getenv('ALLOWED_HOSTS', '*').split(',')]
    
    # Security
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
```

#### 2. Configure no DigitalOcean

1. Acesse [DigitalOcean App Platform](https://cloud.digitalocean.com/apps)
2. Clique em "Create App"
3. Conecte seu repositório GitHub/GitLab
4. Configure:
   - **Build Command:** `pip install -r requirements.txt`
   - **Run Command:** `gunicorn marcenaria.wsgi:application --bind 0.0.0.0:$PORT`

#### 3. Adicione Variáveis de Ambiente

No painel do App Platform, adicione:
- `SECRET_KEY`
- `DEBUG=False`
- `ALLOWED_HOSTS=seu-dominio.com`
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_STORAGE_BUCKET_NAME`
- `AWS_S3_REGION_NAME`
- `AWS_S3_ENDPOINT_URL`
- `WHATSAPP_API_TOKEN`
- `WHATSAPP_PHONE_NUMBER_ID`

#### 4. Adicione Gunicorn

Atualize `requirements.txt`:
```
Django>=5.0,<6.0
boto3
requests
pillow
reportlab
weasyprint
python-dotenv
gunicorn
```

#### 5. Deploy
Clique em "Deploy" e aguarde o build.

---

### Opção 2: Railway

#### 1. Instale o Railway CLI
```bash
npm i -g @railway/cli
```

#### 2. Login e Deploy
```bash
railway login
railway init
railway up
```

#### 3. Configure Variáveis de Ambiente
```bash
railway variables set SECRET_KEY=sua-chave
railway variables set DEBUG=False
# ... adicione todas as outras variáveis
```

---

### Opção 3: Render

#### 1. Crie `build.sh`
```bash
#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
```

Torne executável:
```bash
chmod +x build.sh
```

#### 2. Configure no Render

1. Acesse [Render](https://render.com)
2. Crie um novo "Web Service"
3. Conecte seu repositório
4. Configure:
   - **Build Command:** `./build.sh`
   - **Start Command:** `gunicorn marcenaria.wsgi:application`
   - **Environment:** Python 3

#### 3. Adicione Variáveis de Ambiente
No painel do Render, adicione todas as variáveis do `.env`.

---

## 🔧 Configurações Adicionais

### DigitalOcean Spaces

1. Acesse [DigitalOcean Spaces](https://cloud.digitalocean.com/spaces)
2. Crie um novo Space
3. Gere as chaves de API em "API" → "Spaces Keys"
4. Configure CORS (opcional):
```json
[
  {
    "AllowedOrigins": ["*"],
    "AllowedMethods": ["GET", "PUT", "POST"],
    "AllowedHeaders": ["*"],
    "MaxAgeSeconds": 3000
  }
]
```

### WhatsApp Business API

1. Acesse [Meta for Developers](https://developers.facebook.com/)
2. Crie um App
3. Adicione o produto "WhatsApp"
4. Configure o número de telefone
5. Gere o token de acesso permanente
6. Copie o `Phone Number ID`

---

## 📊 Monitoramento e Logs

### Logs Locais
```bash
python manage.py runserver --verbosity 2
```

### Logs em Produção (DigitalOcean)
```bash
doctl apps logs <app-id>
```

### Logs em Produção (Railway)
```bash
railway logs
```

---

## 🔐 Segurança

### Gere uma SECRET_KEY Segura
```python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Checklist de Segurança
- [ ] `DEBUG=False` em produção
- [ ] `SECRET_KEY` única e segura
- [ ] `ALLOWED_HOSTS` configurado corretamente
- [ ] HTTPS habilitado
- [ ] Variáveis de ambiente protegidas
- [ ] Backup regular do banco de dados

---

## 🗄️ Backup do Banco de Dados

### Backup Local (SQLite)
```bash
cp db.sqlite3 backup_$(date +%Y%m%d).sqlite3
```

### Migração para PostgreSQL (Produção)

1. Instale psycopg2:
```bash
pip install psycopg2-binary
```

2. Atualize `settings.py`:
```python
import dj_database_url

DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv('DATABASE_URL'),
        conn_max_age=600
    )
}
```

3. Adicione ao `requirements.txt`:
```
dj-database-url
psycopg2-binary
```

---

## 📱 Teste o Deploy

1. Acesse a URL do deploy
2. Faça login com o superusuário
3. Teste o fluxo completo:
   - Criar cliente
   - Criar orçamento
   - Upload de imagem
   - Gerar PDF
   - Enviar WhatsApp

---

## 🆘 Troubleshooting

### Erro: "DisallowedHost"
Adicione seu domínio ao `ALLOWED_HOSTS` no `.env`.

### Erro: "Static files not found"
Execute:
```bash
python manage.py collectstatic
```

### Erro: "S3 Upload Failed"
Verifique:
- Credenciais corretas
- Endpoint URL correto
- Bucket existe e tem permissões

### Erro: "WhatsApp API Error"
Verifique:
- Token válido
- Phone Number ID correto
- Número do cliente no formato internacional (+5511999999999)

---

## 📞 Suporte

Para dúvidas ou problemas:
1. Verifique os logs da aplicação
2. Consulte a documentação do Django
3. Revise as configurações de ambiente

**Boa sorte com o deploy! 🚀**
