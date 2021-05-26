from typing import List

from django.utils.translation import gettext as _

from baronbale_website.banner_parser.business import (
    banner_parser,
    banner_sorter,
)

MARGIN_BETWEEN_BANNER = 0.5


def render_banners_to_html(
    banners: List[dict], horizontal_banners_per_row: int, vertical_banners_per_row: int
) -> str:
    banners_html: str = _join_banners(
        banners, horizontal_banners_per_row, vertical_banners_per_row
    )
    banners_html += (
        "<p>"
        + _("The bannerlist was generated on")
        + ' <a href="https://baronbale.de/tools/gc/banner/">baronbale.de</a>'
        + "</p>"
    )
    return banners_html


def _join_banners(
    banners: List[dict], horizontal_banners_per_row: int, vertical_banners_per_row: int
) -> str:
    joined_banners = ""
    balanced_output = False

    for idx, banner in enumerate(banners):
        if banner[banner_sorter.RATIO_TAG] > 1.0:  # if horizontal
            joined_banners += (
                _get_formatted_banner(banner, horizontal_banners_per_row) + "\n"
            )
        elif (
            not balanced_output
            and idx % horizontal_banners_per_row > 0
            and banner[banner_sorter.RATIO_TAG] <= 1.0
        ):
            joined_banners += (
                _get_formatted_banner(banner, horizontal_banners_per_row) + "\n"
            )
            if idx % horizontal_banners_per_row == horizontal_banners_per_row - 1:
                balanced_output = True
        else:
            joined_banners += (
                _get_formatted_banner(banner, vertical_banners_per_row) + "\n"
            )
            balanced_output = True

    return joined_banners + "\n"


def _get_formatted_banner(banner: dict, banner_per_row: int):
    return banner_parser.BANNER_TEMPLATE.format(
        banner[banner_parser.HREF_TAG],
        banner[banner_parser.SRC_TAG],
        _calculate_banner_width(banner_per_row),
    )


def _calculate_banner_width(banners_per_row: int):
    return round(100 / banners_per_row - MARGIN_BETWEEN_BANNER, 2)
