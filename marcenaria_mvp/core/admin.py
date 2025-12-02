from django.contrib import admin
from .models import Cliente, Orcamento

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'whatsapp', 'email', 'created_at')
    search_fields = ('nome', 'whatsapp', 'email')
    list_filter = ('created_at',)

@admin.register(Orcamento)
class OrcamentoAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'data_criacao', 'total', 'status')
    list_filter = ('status', 'data_criacao')
    search_fields = ('cliente__nome',)
    readonly_fields = ('data_criacao',)
