from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView, ListView, DeleteView

from app_mailing.forms import MailingForm
from app_mailing.models import Mailing


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        new_obj: Mailing = form.save(commit=False)
        new_obj.mailing_owner = self.request.user
        new_obj.save()
        for subscriber in form.cleaned_data['subscribers']:
            new_obj.subscribers.add(subscriber)
        new_obj.save()
        return redirect(new_obj.get_absolute_url())


class MailingDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Mailing

    def test_func(self):
        curr_user = self.request.user
        return self.get_object().mailing_owner == curr_user


class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing


    def get_queryset(self):
        queryset = super().get_queryset().filter(mailing_owner=self.request.user)
        return queryset


class MailingUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Mailing
    form_class = MailingForm

    def test_func(self):
        curr_user = self.request.user
        return self.get_object().mailing_owner == curr_user

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class MailingDeleteView(LoginRequiredMixin, UserPassesTestMixin,  DeleteView):
    model = Mailing
    success_url = reverse_lazy('app_mailings:mailing_list')


    def test_func(self):
        curr_user = self.request.user
        return self.get_object().mailing_owner == curr_user

    def get_template_names(self):
        return 'shared/model_confirm_delete.html'
