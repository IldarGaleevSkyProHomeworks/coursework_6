from django import forms

from app_mailing.models import Mailing, MailMessage


class MailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = '__all__'


class MailMessageForm(forms.ModelForm):
    class Meta:
        model = MailMessage
        fields = '__all__'
