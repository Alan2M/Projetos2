from django import forms

class FiltroAlunoForm(forms.Form):
    nome = forms.CharField(required=False, label="Nome")
    email = forms.EmailField(required=False, label="Email")
    serie = forms.CharField(required=False, label="Série")
    data_inscricao = forms.DateField(
        required=False, 
        label="Data de Inscrição",
        widget=forms.DateInput(attrs={'type': 'date'})
    )