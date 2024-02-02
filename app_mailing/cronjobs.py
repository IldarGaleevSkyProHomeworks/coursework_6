from smtplib import SMTPDataError

from django.core.mail import send_mail

from app_logging.services import report_mailing, REPORT_WARNING, REPORT_FAIL, REPORT_SUCCESS
from app_mailing.models import Mailing

from datetime import datetime


def launch_new_mailings():
    curr_date = datetime.now()

    mailing_new = Mailing.objects.filter(
        mailing_status=Mailing.MailingStatusChoice.CREATED,
        date_start__lte=curr_date,
        date_finish__gte=curr_date
    )

    if mailing_new.exists():
        for new_mailing in mailing_new:
            new_mailing.mailing_status = Mailing.MailingStatusChoice.STARTED
            new_mailing.save()


def stop_finished_mailings():
    curr_date = datetime.now()

    mailings_finished = Mailing.objects.filter(
        mailing_status=Mailing.MailingStatusChoice.STARTED,
        date_finish__lt=curr_date
    )

    if mailings_finished.exists():
        for new_mailing in mailings_finished:
            new_mailing.mailing_status = Mailing.MailingStatusChoice.FINISHED
            new_mailing.save()


def prepare_mailings():
    launch_new_mailings()
    stop_finished_mailings()


def send_mail_job(periodicity: Mailing.PeriodicityChoice):

    def send_report(mailing, reports):
        err_count = len([err for err,_ in reports if err])
        total_count = len(reports)
        if err_count == total_count:
            parent_report = report_mailing(
                mailing=mailing,
                message=f'Ни одно сообщение не было отправлено',
                report_status=REPORT_FAIL
            )
        elif err_count > 0:
            parent_report = report_mailing(
                mailing=mailing,
                message=f'Отправка {err_count} из {total_count} сообщений завершились ошибкой',
                report_status=REPORT_WARNING
            )
        else:
            parent_report = report_mailing(
                mailing=mailing,
                message=f'Отправка {err_count} из {total_count} сообщений завершились ошибкой',
                report_status=REPORT_SUCCESS
            )

        for err, recipient in reports:
            report_mailing(
                mailing=mailing,
                exception=err,
                recipient=recipient,
                parent_report=parent_report
            )

    def _wrap():
        prepare_mailings()
        mailing_list = Mailing.objects.filter(
            mailing_status=Mailing.MailingStatusChoice.STARTED,
            periodicity=periodicity
        )

        if mailing_list.exists():
            for mailing in mailing_list:
                msg = mailing.message
                subscribers = mailing.subscribers.all()
                reports = []
                for subscriber in subscribers:
                    try:
                        send_mail(
                            subject=msg.subject,
                            message=msg.text,
                            from_email=mailing.mailing_owner.email,
                            recipient_list=(subscriber.email,))

                        reports.append((None, subscriber))

                    except (SMTPDataError,) as send_mail_error:
                        reports.append((send_mail_error, subscriber))
                send_report(mailing, reports)

    return _wrap


schedule_daily = send_mail_job(Mailing.PeriodicityChoice.DAILY)
schedule_weekly = send_mail_job(Mailing.PeriodicityChoice.WEEKLY)
schedule_monthly = send_mail_job(Mailing.PeriodicityChoice.MONTHLY)
