from django import forms 

class SearchFrom(forms.Form):
    my_attrs = {'class' : 'form-control input'}
    date_attrs = {'class' : 'form-control input', 'type' : 'date'}
    city = forms.CharField(label="Dove andiamo?", max_length=20, 
        widget = forms.TextInput(attrs = my_attrs)
    )
    start = forms.DateField(label='Partenza',
        widget = forms.TextInput(attrs = date_attrs)
    )
    end = forms.DateField(label='Ritorno',
        widget = forms.TextInput(attrs = date_attrs)
    )
    how_many = forms.CharField(label='Persone', 
        widget = forms.TextInput(attrs = my_attrs)
    )