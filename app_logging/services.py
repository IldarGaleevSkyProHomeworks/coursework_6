from app_accounts.models import User
from app_logging.models import MailingReport
from app_mailing.models import Mailing

REPORT_SUCCESS = MailingReport.ReportStatus.SUCCESS
REPORT_WARNING = MailingReport.ReportStatus.WARNING
REPORT_FAIL = MailingReport.ReportStatus.FAIL


def report_mailing(
        exception: Exception = None,
        mailing: Mailing = None,
        recipient: User = None,
        message: str = None,
        report_status: MailingReport.ReportStatus = None,
        parent_report: MailingReport = None,
) -> MailingReport:

    report_status = report_status or REPORT_SUCCESS if exception is None else REPORT_FAIL
    if message:
        message = f'{mailing}: {message}'
    else:
        message = f'{mailing}: {recipient.email if recipient else "-"}'

    if exception:
        message += f'\n{exception}'

    report = MailingReport.objects.create(
        mailing=mailing,
        report_status=report_status,
        recipient=recipient,
        report_message=message,
        parent_report=parent_report,
    )

    report.save()
    return report
