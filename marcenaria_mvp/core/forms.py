from django import forms
from .models import Cliente, Orcamento

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
    itens = forms.CharField(required=False, widget=forms.HiddenInput())
    imagens = forms.CharField(required=False, widget=forms.HiddenInput())
    
    class Meta:
        model = Orcamento
        fields = ['cliente', 'status', 'itens', 'imagens', 'total']
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'total': forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
        }
    
    def clean_itens(self):
        import json
        data = self.cleaned_data.get('itens', '[]')
        if not data:
            return []
        try:
            return json.loads(data)
        except json.JSONDecodeError:
            return []
    
    def clean_imagens(self):
        import json
        data = self.cleaned_data.get('imagens', '[]')
        if not data:
            return []
        try:
            return json.loads(data)
        except json.JSONDecodeError:
            return []

