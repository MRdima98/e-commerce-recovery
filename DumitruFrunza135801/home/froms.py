from django import forms 

class SearchFrom(forms.Form):
    city = forms.CharField(label=None, max_length=20, 
        widget=forms.TextInput(
            attrs={
                'class' : 'form-control input' 
            }
        )
    )