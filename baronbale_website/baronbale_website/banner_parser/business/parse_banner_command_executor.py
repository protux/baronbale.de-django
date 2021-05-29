from typing import Optional
from datetime import (
    datetime,
    timedelta,
)

from baronbale_website.banner_parser.business import job_worker
from baronbale_website.banner_parser.models import BannerParserJob


def parse_banners() -> None:
    if not _is_job_active():
        next_job_ticket_id_to_work_on_query_set = _get_next_job_ticket_id_to_work_on()
        if next_job_ticket_id_to_work_on_query_set:
            job_worker.find_banners_from_banner_parser_job(
                next_job_ticket_id_to_work_on_query_set
            )


def _is_job_active() -> bool:
    earliest_as_active_accepted_datetime = _get_earliest_as_active_accepted_datetime()

    active_banner_parser_job_query = BannerParserJob.objects.filter(
        actively_working_on_since__isnull=False,
        actively_working_on_since__gte=earliest_as_active_accepted_datetime,
        result__isnull=True,
    )
    return active_banner_parser_job_query.exists()


def _get_earliest_as_active_accepted_datetime() -> datetime:
    now = datetime.utcnow()
    earliest_as_active_accepted_datetime = now - timedelta(hours=3)
    return earliest_as_active_accepted_datetime


def _get_next_job_ticket_id_to_work_on() -> Optional[str]:
    try:
        return (
            BannerParserJob.objects.values_list("ticket_id", flat=True)
            .order_by("id")
            .filter(actively_working_on_since__isnull=True, result__isnull=True)
            .first()
        )
    except BannerParserJob.DoesNotExist:
        return None
