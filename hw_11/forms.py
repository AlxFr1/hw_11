import datetime

from django import forms
from django.core.exceptions import ValidationError


class CeleryForm(forms.Form):
    email = forms.EmailField()
    question = forms.CharField(max_length=30)
    reminder_date = forms.DateField(required=True, input_formats=['%Y-%m-%d %H-%M'])

    def clean_reminder_date(self):
        data = self.cleaned_data['reminder_date']
        if data < datetime.date.today():
            raise ValidationError('Invalid date - renewal in past')
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError('Invalid date - renewal more than 4 weeks ahead')
        return data




#input_formats=['%Y-%m-%d %H-%M']
# class CeleryForm(forms.Form):
#     email = forms.EmailField()
#     question = forms.CharField(max_length=30)
#     date = forms.DateTimeField(label='when to remind ?', required=True, input_formats=['%Y-%m-%d %H-%M'])

