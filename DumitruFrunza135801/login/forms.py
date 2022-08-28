from django import forms 

class RegisterForm(forms.Form):
    base_widget = forms.TextInput({'class': 'form-control base-height'})
    username = forms.CharField(label='Nome utente', widget=base_widget)
    passwd = forms.CharField(label='Password', widget=base_widget)
    confirm_passwd = forms.CharField(label='Conferma password', widget=base_widget)
    email = forms.CharField(label='Email', widget=base_widget)
    name = forms.CharField(label='Nome', widget=base_widget)
    surname = forms.CharField(label='Cognome', widget=base_widget)