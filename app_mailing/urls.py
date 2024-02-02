from app_mailing.apps import AppMailingConfig
from django.urls import path

from app_mailing.views import (MailingCreateView, MailingDetailView, MailingListView, MailingUpdateView,
                               MailingDeleteView)

app_name = AppMailingConfig.name

urlpatterns = [
    path('', MailingListView.as_view(), name='mailing_list'),
    path('/create', MailingCreateView.as_view(), name='mailing_create'),
    path('<int:pk>/', MailingDetailView.as_view(), name='mailing_detail'),
    path('<int:pk>/update', MailingUpdateView.as_view(), name='mailing_update'),
    path('<int:pk>/delete', MailingDeleteView.as_view(), name='mailing_delete'),
]
