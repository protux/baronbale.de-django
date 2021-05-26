from datetime import datetime
import logging
from typing import List

from baronbale_website.banner_parser.models import BannerParserJob
from baronbale_website.banner_parser.business.utils import file_extractor
from baronbale_website.banner_parser.business import (
    banner_parser,
    banner_result_renderer,
    banner_sorter,
)

logger = logging.getLogger(__name__)


def find_banners_from_banner_parser_job(ticket_id: str) -> None:
    try:
        BannerParserJob.objects.filter(ticket_id=ticket_id).update(
            actively_working_on_since=datetime.utcnow()
        )
        banner_parser_job = BannerParserJob.objects.get(ticket_id=ticket_id)
        banners_html = _parse_banners(banner_parser_job)
        _persist_result(banner_parser_job, banners_html)
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
