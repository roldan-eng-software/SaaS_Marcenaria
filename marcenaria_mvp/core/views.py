from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Cliente, Orcamento
from .forms import ClienteForm, OrcamentoForm, ItemOrcamentoFormSet, ImagemOrcamentoFormSet
import json
import logging
from django.template.loader import render_to_string
from django.conf import settings
import requests
import boto3

logger = logging.getLogger(__name__)

from django.db.models import Sum

@login_required
def dashboard(request):
    orcamentos_pendentes = Orcamento.objects.filter(user=request.user, status='rascunho').count()
    clientes_novos = Cliente.objects.filter(user=request.user).count()
    receita = Orcamento.objects.filter(user=request.user, status='aprovado').aggregate(Sum('total'))['total__sum'] or 0
    
    return render(request, 'dashboard.html', {
        'orcamentos_pendentes': orcamentos_pendentes,
        'clientes_novos': clientes_novos,
        'receita': receita
    })

@login_required
def clientes_list(request):
    query = request.GET.get('q')
    if query:
        clientes = Cliente.objects.filter(user=request.user, nome__icontains=query)
    else:
        clientes = Cliente.objects.filter(user=request.user)
    return render(request, 'clientes_list.html', {'clientes': clientes})

@login_required
def cliente_create(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            cliente = form.save(commit=False)
            cliente.user = request.user
            cliente.save()
            return redirect('clientes_list')
    else:
        form = ClienteForm()
    return render(request, 'cliente_form.html', {'form': form})

@login_required
def cliente_edit(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('clientes_list')
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'cliente_form.html', {'form': form})

@login_required
def orcamento_list(request):
    status_filter = request.GET.get('status')
    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')
    
    orcamentos = Orcamento.objects.filter(user=request.user).select_related('cliente')
    
    if status_filter:
        orcamentos = orcamentos.filter(status=status_filter)
    
    if data_inicio:
        orcamentos = orcamentos.filter(data_criacao__date__gte=data_inicio)
        
    if data_fim:
        orcamentos = orcamentos.filter(data_criacao__date__lte=data_fim)
        
    return render(request, 'orcamento_list.html', {'orcamentos': orcamentos})

@login_required
def orcamento_create(request):
    if request.method == 'POST':
        form = OrcamentoForm(request.POST)
        item_formset = ItemOrcamentoFormSet(request.POST, instance=Orcamento())
        imagem_formset = ImagemOrcamentoFormSet(request.POST, request.FILES, instance=Orcamento())
        if form.is_valid() and item_formset.is_valid() and imagem_formset.is_valid():
            orcamento = form.save(commit=False)
            orcamento.user = request.user
            orcamento.save()
            item_formset.instance = orcamento
            item_formset.save()
            imagem_formset.instance = orcamento
            imagem_formset.save()
            return redirect('orcamento_detail', pk=orcamento.id)
        else:
            logger.error("Form errors: %s", form.errors)
            logger.debug("POST data: %s", request.POST)
    else:
        form = OrcamentoForm()
        item_formset = ItemOrcamentoFormSet(instance=Orcamento())
        imagem_formset = ImagemOrcamentoFormSet(instance=Orcamento())
    return render(request, 'orcamento_form.html', {'form': form, 'item_formset': item_formset, 'imagem_formset': imagem_formset})

@login_required
def orcamento_edit(request, pk):
    orcamento = get_object_or_404(Orcamento, pk=pk, user=request.user)
    if request.method == 'POST':
        form = OrcamentoForm(request.POST, instance=orcamento)
        item_formset = ItemOrcamentoFormSet(request.POST, instance=orcamento)
        imagem_formset = ImagemOrcamentoFormSet(request.POST, request.FILES, instance=orcamento)
        if form.is_valid() and item_formset.is_valid() and imagem_formset.is_valid():
            form.save()
            item_formset.save()
            imagem_formset.save()
            return redirect('orcamento_detail', pk=pk)
        else:
            logger.error("Form errors: %s", form.errors)
    else:
        form = OrcamentoForm(instance=orcamento)
        item_formset = ItemOrcamentoFormSet(instance=orcamento)
        imagem_formset = ImagemOrcamentoFormSet(instance=orcamento)
    return render(request, 'orcamento_form.html', {'form': form, 'item_formset': item_formset, 'imagem_formset': imagem_formset, 'orcamento': orcamento})

@login_required
def orcamento_detail(request, pk):
    orcamento = get_object_or_404(Orcamento, pk=pk, user=request.user)
    return render(request, 'orcamento_detail.html', {'orcamento': orcamento})

@login_required
def orcamento_update_status(request, pk):
    if request.method == 'POST':
        orcamento = get_object_or_404(Orcamento, pk=pk, user=request.user)
        new_status = request.POST.get('status')
        if new_status in ['rascunho', 'enviado', 'aprovado']:
            orcamento.status = new_status
            orcamento.save()
    return redirect('orcamento_detail', pk=pk)

@login_required
def orcamento_pdf(request, pk):
    from django.http import HttpResponse
    from weasyprint import HTML
    orcamento = get_object_or_404(Orcamento, pk=pk, user=request.user)
    html = render_to_string('orcamento_pdf.html', {'orcamento': orcamento})
    pdf_bytes = HTML(string=html).write_pdf()
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="orcamento_{orcamento.id}.pdf"'
    return response

@login_required
def orcamento_enviar(request, pk):
    from django.contrib import messages
    from weasyprint import HTML
    orcamento = get_object_or_404(Orcamento, pk=pk, user=request.user)
    try:
        html = render_to_string('orcamento_pdf.html', {'orcamento': orcamento})
        pdf_bytes = HTML(string=html).write_pdf()

        bucket = settings.AWS_STORAGE_BUCKET_NAME
        if not bucket:
            messages.error(request, 'Bucket S3 não configurado.')
            return redirect('orcamento_detail', pk=pk)

        s3 = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_S3_REGION_NAME,
            endpoint_url=settings.AWS_S3_ENDPOINT_URL,
        )
        key = f"orcamentos/orcamento_{orcamento.id}.pdf"
        s3.put_object(Bucket=bucket, Key=key, Body=pdf_bytes, ContentType='application/pdf')
        presigned_url = s3.generate_presigned_url(
            'get_object', Params={'Bucket': bucket, 'Key': key}, ExpiresIn=3600
        )

        token = settings.WHATSAPP_API_TOKEN
        phone_id = settings.WHATSAPP_PHONE_NUMBER_ID
        if not token or not phone_id:
            messages.error(request, 'Credenciais WhatsApp não configuradas.')
            return redirect('orcamento_detail', pk=pk)

        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json',
        }
        payload = {
            'messaging_product': 'whatsapp',
            'to': orcamento.cliente.whatsapp,
            'type': 'text',
            'text': {
                'preview_url': True,
                'body': f"Olá {orcamento.cliente.nome}! Seu orçamento: {presigned_url}",
            },
        }
        url = f"https://graph.facebook.com/v20.0/{phone_id}/messages"
        resp = requests.post(url, headers=headers, json=payload, timeout=20)
        if resp.status_code >= 200 and resp.status_code < 300:
            orcamento.status = 'enviado'
            orcamento.save()
            messages.success(request, 'Orçamento enviado via WhatsApp com sucesso.')
        else:
            logger.error('Erro WhatsApp: %s', resp.text)
            messages.error(request, 'Falha ao enviar WhatsApp. Verifique credenciais e formato do número.')
    except Exception as e:
        logger.exception('Falha ao gerar/enviar orçamento: %s', e)
        from django.contrib import messages
        messages.error(request, 'Erro ao processar envio do orçamento.')
    return redirect('orcamento_detail', pk=pk)
