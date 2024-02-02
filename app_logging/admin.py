from django.contrib import admin

from app_logging.models import MailingReport


class ChildReportsInline(admin.TabularInline):
    model = MailingReport
    can_delete = False

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj):
        return False


@admin.register(MailingReport)
class MailingReportAdmin(admin.ModelAdmin):
    list_display = ['report_status', 'report_date_time', 'mailing']
    list_filter = ['report_status']
    search_fields = ['report_date_time', 'report_message']
    inlines = [
        ChildReportsInline
    ]

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    # def has_delete_permission(self, request, obj=None):
    #     return False
