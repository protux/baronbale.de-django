import hashlib
import logging
from datetime import datetime
from typing import List

from django.conf import settings
from django.core import mail
from smtplib import SMTPException

from baronbale_website.banner_parser.business import (
    banner_parser,
    banner_result_renderer,
    banner_sorter,
)
from baronbale_website.banner_parser.business.utils import (
    file_extractor,
    mail_renderer,
)
from baronbale_website.banner_parser.models import BannerParserJob

logger = logging.getLogger(__name__)


def find_banners_from_banner_parser_job(ticket_id: str) -> None:
    try:
        BannerParserJob.objects.filter(ticket_id=ticket_id).update(
            actively_working_on_since=datetime.utcnow()
        )
        banner_parser_job = BannerParserJob.objects.get(ticket_id=ticket_id)
        banners_html = _parse_banners(banner_parser_job)
        _persist_result(banner_parser_job, banners_html)
        _send_job_finished_mail(banner_parser_job)
    except Exception:
        logger.exception("Error while parsing banners.")
        BannerParserJob.objects.filter(ticket_id=ticket_id).update(
            actively_working_on_since=None
        )


def _parse_banners(banner_parser_job: BannerParserJob) -> str:
    extracted_files: List[str] = file_extractor.extract_gpx_if_needed(
        banner_parser_job.uploaded_file
    )
    banners: List[dict] = banner_parser.collect_banner_urls(extracted_files)
    sorted_banners: List[dict] = banner_sorter.sort_banner(banners)
    banners_html: str = banner_result_renderer.render_banners_to_html(
        sorted_banners,
        banner_parser_job.horizontal_banners_per_row,
        banner_parser_job.vertical_banners_per_row,
    )
    return banners_html


def _persist_result(banner_parser_job: BannerParserJob, banners_html: str) -> None:
    banner_parser_job.time_finished = datetime.utcnow()
    banner_parser_job.result = banners_html
    banner_parser_job.save()


def _send_job_finished_mail(banner_parser_job: BannerParserJob) -> None:
    if banner_parser_job.email_address_to_notify:
        mail_body: str = mail_renderer.render_mail_body(banner_parser_job)
        subject: str = "Deine Banner von baronbale.de sind fertig!"

        try:
            mail.send_mail(
                subject=subject,
                message=mail_body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[banner_parser_job.email_address_to_notify],
                fail_silently=False,
            )
        finally:
            banner_parser_job.email_address_to_notify = hashlib.sha256(
                banner_parser_job.email_address_to_notify.encode("UTF-8")
            ).hexdigest()
            banner_parser_job.save()
