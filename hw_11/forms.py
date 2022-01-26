import datetime

from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone


class CeleryForm(forms.Form):
    email = forms.EmailField()
    question = forms.CharField(max_length=30)
    reminder_date = forms.DateTimeField(required=True, label='DateTime')

    def clean_reminder_date(self):
        data = self.cleaned_data['reminder_date'] - datetime.timedelta(hours=2) + datetime.timedelta(milliseconds=1)
        if data < timezone.now():
            raise ValidationError('Invalid date - renewal in past')
        if data > timezone.now() + datetime.timedelta(days=2):
            raise ValidationError('Invalid date - renewal more than 2 days ahead')
        return data
