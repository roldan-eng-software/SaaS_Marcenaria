from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Cliente, Orcamento
from .forms import ClienteForm, OrcamentoForm
import json

@login_required
def dashboard(request):
    orcamentos_pendentes = Orcamento.objects.filter(status='rascunho').count()
    clientes_novos = Cliente.objects.count()
    # Calculate total revenue from approved budgets
    receita = sum(orc.total for orc in Orcamento.objects.filter(status='aprovado'))
    
    return render(request, 'dashboard.html', {
        'orcamentos_pendentes': orcamentos_pendentes,
        'clientes_novos': clientes_novos,
        'receita': receita
    })

@login_required
def clientes_list(request):
    query = request.GET.get('q')
    if query:
        clientes = Cliente.objects.filter(nome__icontains=query)
    else:
        clientes = Cliente.objects.all()
    return render(request, 'clientes_list.html', {'clientes': clientes})

@login_required
def cliente_create(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('clientes_list')
    else:
        form = ClienteForm()
    return render(request, 'cliente_form.html', {'form': form})

@login_required
def orcamento_list(request):
    status_filter = request.GET.get('status')
    if status_filter:
        orcamentos = Orcamento.objects.filter(status=status_filter)
    else:
        orcamentos = Orcamento.objects.all()
    return render(request, 'orcamento_list.html', {'orcamentos': orcamentos})

@login_required
def orcamento_create(request):
    if request.method == 'POST':
        form = OrcamentoForm(request.POST)
        if form.is_valid():
            orcamento = form.save(commit=False)
            # Ensure JSON fields are properly saved (Django form cleaning should handle this if valid JSON string)
            orcamento.save()
            return redirect('orcamento_list')
    else:
        form = OrcamentoForm()
    return render(request, 'orcamento_form.html', {'form': form})

@login_required
def orcamento_edit(request, pk):
    orcamento = get_object_or_404(Orcamento, pk=pk)
    if request.method == 'POST':
        form = OrcamentoForm(request.POST, instance=orcamento)
        if form.is_valid():
            form.save()
            return redirect('orcamento_list')
    else:
        form = OrcamentoForm(instance=orcamento)
    return render(request, 'orcamento_form.html', {'form': form, 'orcamento': orcamento})
