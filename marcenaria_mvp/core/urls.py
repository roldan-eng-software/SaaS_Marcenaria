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
    path('clientes/<int:pk>/editar/', views.cliente_edit, name='cliente_edit'),
    
    # Orçamentos
    path('orcamentos/', views.orcamento_list, name='orcamento_list'),
    path('orcamentos/novo/', views.orcamento_create, name='orcamento_create'),
    path('orcamentos/<int:pk>/', views.orcamento_detail, name='orcamento_detail'),
    path('orcamentos/<int:pk>/editar/', views.orcamento_edit, name='orcamento_edit'),
    path('orcamentos/<int:pk>/enviar/', views.orcamento_enviar, name='orcamento_enviar'),
    path('orcamentos/<int:pk>/pdf/', views.orcamento_pdf, name='orcamento_pdf'),
    path('orcamentos/<int:pk>/status/', views.orcamento_update_status, name='orcamento_update_status'),
]
