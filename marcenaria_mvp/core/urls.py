from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Clientes
    path('clientes/', views.clientes_list, name='clientes_list'),
    path('clientes/novo/', views.cliente_create, name='cliente_create'),
    
    # Orçamentos
    path('orcamentos/', views.orcamento_list, name='orcamento_list'),
    path('orcamentos/novo/', views.orcamento_create, name='orcamento_create'),
    path('orcamentos/<int:pk>/editar/', views.orcamento_edit, name='orcamento_edit'),
]
