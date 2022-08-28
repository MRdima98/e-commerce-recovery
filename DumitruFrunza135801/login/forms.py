from django import forms 

class RegisterForm(forms.Form):
    base_widget = forms.TextInput({'class': 'form-control base-height light-bottom-margin'})
    username = forms.CharField(label='Nome utente', widget=base_widget)
    email = forms.CharField(label='Email', widget=forms.TextInput({
            'class': 'form-control base-height light-bottom-margin',
            'type' : 'email'
        }))
    passwd = forms.CharField(label='Password', widget=forms.TextInput({
            'class': 'form-control base-height light-bottom-margin',
            'type' : 'password'
        }))
    confirm_passwd = forms.CharField(label='Conferma password', 
        widget=forms.TextInput({
            'class': 'form-control base-height light-bottom-margin',
            'type' : 'password'}))
    name = forms.CharField(label='Nome', widget=base_widget)
    surname = forms.CharField(label='Cognome', widget=base_widget)