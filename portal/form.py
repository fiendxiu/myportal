from django import forms
from django.forms import ModelForm,Textarea,Select
from django.forms.fields import ChoiceField
from portal.models import *

class Reportform(forms.Form):
    username = forms.CharField(max_length=20)
    fileurl = forms.FileField()

class Customerform(ModelForm):
    class Meta:
        model = Customer
        exclude = ['mod_date']

    def __init__(self, *args, **kwargs):
        super(Customerform, self).__init__(*args, **kwargs)
        for field_name in self.fields:
            field = self.fields[field_name]
            if field_name == 'username':
                field.widget.attrs.update({'class':'form-control','disabled':True})
            else:
                field.widget.attrs.update({'class':'form-control'})

class Netflowform(ModelForm):
    class Meta:
        model = Netflow
        exclude = ['mod_date']

    def __init__(self, *args, **kwargs):
        super(Netflowform, self).__init__(*args, **kwargs)
        for field_name in self.fields:
            field = self.fields[field_name]
            if field_name == 'username':
                field.widget.attrs.update({'class':'form-control','disabled':True})
            else:
                field.widget.attrs.update({'class':'form-control'})

class Cactiform(ModelForm):
    class Meta:
        model = Cacti
        exclude = ['mod_date']

    def __init__(self, *args, **kwargs):
        super(Cactiform, self).__init__(*args, **kwargs)
        for field_name in self.fields:
            field = self.fields[field_name]
            if field_name == 'username':
                field.widget.attrs.update({'class':'form-control','disabled':True})
            else:
                field.widget.attrs.update({'class':'form-control'})

class Availabilityform(ModelForm):
    class Meta:
        model = Availability
        exclude = ['mod_date']

    def __init__(self, *args, **kwargs):
        super(Availabilityform, self).__init__(*args, **kwargs)
        for field_name in self.fields:
            field = self.fields[field_name]
            if field_name == 'username':
                field.widget.attrs.update({'class':'form-control','disabled':True})
            else:
                field.widget.attrs.update({'class':'form-control'})
