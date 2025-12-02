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
            orcamento.save()
            return redirect('orcamento_list')
        else:
            # Print errors to console for debugging
            print("Form errors:", form.errors)
            print("POST data:", request.POST)
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

@login_required
def orcamento_pdf(request, pk):
    from django.http import HttpResponse
    from reportlab.lib.pagesizes import A4
    from reportlab.lib import colors
    from reportlab.lib.units import cm
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_CENTER, TA_RIGHT
    from io import BytesIO
    
    orcamento = get_object_or_404(Orcamento, pk=pk)
    
    # Create PDF buffer
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=2*cm, leftMargin=2*cm, topMargin=2*cm, bottomMargin=2*cm)
    
    # Container for PDF elements
    elements = []
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#2C5530'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#2C5530'),
        spaceAfter=12,
        borderColor=colors.HexColor('#D4A017'),
        borderWidth=2,
        borderPadding=5
    )
    
    # Title
    elements.append(Paragraph("MARCENARIA PRO", title_style))
    elements.append(Paragraph("Orçamento Profissional", styles['Normal']))
    elements.append(Spacer(1, 20))
    
    # Orçamento Info
    elements.append(Paragraph("Informações do Orçamento", heading_style))
    info_data = [
        ['Número:', f'#{orcamento.id}', 'Data:', orcamento.data_criacao.strftime('%d/%m/%Y')],
        ['Status:', orcamento.get_status_display(), '', '']
    ]
    info_table = Table(info_data, colWidths=[3*cm, 5*cm, 3*cm, 5*cm])
    info_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#2C5530')),
    ]))
    elements.append(info_table)
    elements.append(Spacer(1, 20))
    
    # Cliente Info
    elements.append(Paragraph("Dados do Cliente", heading_style))
    cliente_data = [
        ['Nome:', orcamento.cliente.nome],
        ['WhatsApp:', orcamento.cliente.whatsapp],
    ]
    if orcamento.cliente.email:
        cliente_data.append(['Email:', orcamento.cliente.email])
    if orcamento.cliente.endereco:
        cliente_data.append(['Endereço:', orcamento.cliente.endereco])
    
    cliente_table = Table(cliente_data, colWidths=[4*cm, 12*cm])
    cliente_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#2C5530')),
    ]))
    elements.append(cliente_table)
    elements.append(Spacer(1, 20))
    
    # Itens
    elements.append(Paragraph("Itens do Orçamento", heading_style))
    itens_data = [['Material/Serviço', 'Qtd', 'Preço Unit.', 'Subtotal']]
    
    for item in orcamento.itens:
        subtotal = item['qtd'] * item['preco_unit']
        itens_data.append([
            item['material'],
            str(item['qtd']),
            f"R$ {item['preco_unit']:.2f}",
            f"R$ {subtotal:.2f}"
        ])
    
    # Total row
    itens_data.append(['', '', 'TOTAL:', f"R$ {orcamento.total:.2f}"])
    
    itens_table = Table(itens_data, colWidths=[8*cm, 2*cm, 3*cm, 3*cm])
    itens_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2C5530')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#D4A017')),
        ('TEXTCOLOR', (0, -1), (-1, -1), colors.whitesmoke),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -2), 1, colors.grey),
    ]))
    elements.append(itens_table)
    elements.append(Spacer(1, 30))
    
    # Footer
    footer_style = ParagraphStyle('Footer', parent=styles['Normal'], fontSize=9, textColor=colors.grey, alignment=TA_CENTER)
    elements.append(Paragraph("Este orçamento tem validade de 30 dias a partir da data de emissão.", footer_style))
    elements.append(Paragraph("Marcenaria Pro - Qualidade e Excelência em Marcenaria", footer_style))
    
    # Build PDF
    doc.build(elements)
    
    # Get PDF from buffer
    pdf = buffer.getvalue()
    buffer.close()
    
    # Create HTTP response
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="orcamento_{orcamento.id}.pdf"'
    
    return response

