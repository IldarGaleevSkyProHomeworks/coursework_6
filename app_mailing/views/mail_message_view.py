from django.views.generic import DetailView, CreateView, UpdateView, ListView, DeleteView

from app_mailing.forms import MailMessageForm
from app_mailing.models import MailMessage


class MailMessageCreateView(CreateView):
    model = MailMessage
    form_class = MailMessageForm


class MailMessageDetailView(DetailView):
    model = MailMessage


class MailMessageListView(ListView):
    model = MailMessage


class MailMessageUpdateView(UpdateView):
    model = MailMessage
    form_class = MailMessageForm


class MailMessageDeleteView(DeleteView):
    model = MailMessage

    def get_template_names(self):
        return 'shared/model_confirm_delete.html'
