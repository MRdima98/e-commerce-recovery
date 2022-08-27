from tkinter import Widget
from django import forms
from .models import Activity, Hotel, Rooms, Cost

ACTIVITIES = Activity.objects.all().distinct()

class HotelForm(forms.ModelForm):
    base_widget = forms.TextInput({'class': 'form-control base-height'})
    half_row = 'half_row'
    name = forms.CharField(label='Nome albergo' , max_length = 50,
        widget=base_widget, help_text=half_row)
    IVA = forms.CharField(label='IVA' , max_length =15,
        widget=base_widget, help_text=half_row)
    street = forms.CharField(label='Via' , max_length =50, 
        widget=base_widget, help_text=half_row)
    CAP = forms.DecimalField(label='CAP' , 
        widget=base_widget, help_text=half_row)
    city = forms.CharField(label='Città' , max_length =50,
        widget=base_widget, help_text=half_row)
    stars = forms.DecimalField(label='Stelle' , 
        widget=base_widget, help_text=half_row)
    rooms_count = forms.DecimalField(label='Quante stanze', 
        widget=base_widget, help_text=half_row)
    free_time = forms.CharField(label=None, widget=forms.Textarea(
            attrs={
                'class': 'form-control no-resize',
                'placeholder':'Elencare tutti i possbili passatempo e '
                'attività di svago'}), help_text='Svaghi')
    description = forms.CharField(label=None, widget=forms.Textarea(
        attrs={
            'class': 'form-control no-resize',
            'placeholder':'Descrivere brevemente il tuo '
            'albergo'}), help_text='Description')

    class Meta: 
         model = Hotel 
         fields = [
            'name',
            'IVA',
            'street',
            'CAP',
            'city',
            'stars',
            'rooms_count',
            'free_time',
            'description',
         ]

class RoomsForm(forms.ModelForm):
    attr= {'class': 'form-control base-height'}
    name = forms.CharField(label='Nome camera' , max_length =50, 
        widget = forms.TextInput(attr))
    people = forms.DecimalField(label = None, 
        widget=forms.TextInput(attr))
    size = forms.DecimalField(label = None, 
        widget=forms.TextInput(attr))
    description = forms.CharField(label = None, 
        widget=forms.TextInput(attr))
    photo = forms.FileField(label='Foto')

    class Meta: 
        model = Rooms
        fields = [
            'name',
            'people',
            'size',
            'description',
            'photo'
        ]

class CostForm(forms.ModelForm):
    attr= {'class': 'form-control base-height'}
    cost = forms.DecimalField(widget = forms.TextInput(attr))
    begin_date = forms.DateField(widget=forms.DateInput(
        {'type':'date',
         'class': 'form-control base-height'
        }))
    end_date = forms.DateField(widget=forms.DateInput({
        'type':'date',
        'class': 'form-control base-height'
        }))

    class Meta:
        model = Cost
        fields = [
            'cost',
            'begin_date',
            'end_date'
        ] 

class ActivityForm(forms.Form):
    my_field = forms.MultipleChoiceField(choices=ACTIVITIES, 
        widget=forms.CheckboxSelectMultiple()
    )

