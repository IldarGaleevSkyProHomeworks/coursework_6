from django.views.generic import DetailView, CreateView, UpdateView, ListView, DeleteView

from app_mailing.forms import MailingForm
from app_mailing.models import Mailing


class MailingCreateView(CreateView):
    model = Mailing
    form_class = MailingForm


class MailingDetailView(DetailView):
    model = Mailing


class MailingListView(ListView):
    model = Mailing


class MailingUpdateView(UpdateView):
    model = Mailing
    form_class = MailingForm


class MailingDeleteView(DeleteView):
    model = Mailing

    def get_template_names(self):
        return 'shared/model_confirm_delete.html'
