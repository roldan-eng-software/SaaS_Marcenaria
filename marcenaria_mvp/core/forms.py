from django import forms
from .models import Cliente, Orcamento, ItemOrcamento, ImagemOrcamento
from .widgets import MultipleFileInput

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nome', 'whatsapp', 'email', 'endereco']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'whatsapp': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'endereco': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class OrcamentoForm(forms.ModelForm):
    class Meta:
        model = Orcamento
        fields = ['cliente', 'status', 'total']
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'total': forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
        }

class ItemOrcamentoForm(forms.ModelForm):
    class Meta:
        model = ItemOrcamento
        fields = ['material', 'quantidade', 'preco_unitario']
        widgets = {
            'material': forms.TextInput(attrs={'class': 'form-control'}),
            'quantidade': forms.NumberInput(attrs={'class': 'form-control'}),
            'preco_unitario': forms.NumberInput(attrs={'class': 'form-control'}),
        }

ItemOrcamentoFormSet = forms.inlineformset_factory(
    Orcamento,
    ItemOrcamento,
    form=ItemOrcamentoForm,
    extra=1,
    can_delete=True,
    can_delete_extra=True
)

class ImagemOrcamentoForm(forms.ModelForm):
    class Meta:
        model = ImagemOrcamento
        fields = ['imagem']
        widgets = {
            'imagem': MultipleFileInput(attrs={'class': 'form-control'}),
        }

ImagemOrcamentoFormSet = forms.inlineformset_factory(
    Orcamento,
    ImagemOrcamento,
    form=ImagemOrcamentoForm,
    extra=1,
    can_delete=True,
    can_delete_extra=True
)
