from django import forms

from app_mailing.models import Mailing, MailMessage


class MailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = '__all__'
