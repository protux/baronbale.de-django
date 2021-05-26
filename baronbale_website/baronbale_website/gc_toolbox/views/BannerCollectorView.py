import datetime
import logging
import os
import shutil
import tempfile
import traceback

from django.core import mail
from django.urls import reverse_lazy
from django.utils.translation import ugettext as _
from django.views.generic import FormView

from baronbale_website.common import exceptions, message_utils
from baronbale_website.gc_toolbox import banner_parser, banner_sorter
from baronbale_website.gc_toolbox.forms import UploadGPXForm
from baronbale_website.gc_toolbox.tools.banner_utils import (
    extract_gpx_if_needed,
    join_banners,
)

logger = logging.getLogger("django")

BANNERS_SESSION_KEY = "banners"
TIMER_SESSION_KEY = "banner_timer"
TIMER_FORMAT = "%d.%m.%Y %H:%M%S"


class BannerCollectorView(FormView):
    template_name = "gc_toolbox/banner_collector.html"
    form_class = UploadGPXForm
    success_url = reverse_lazy("gc_toolbox:banner_collector")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        session = self.request.session
        if session:
            banners = session.get(BANNERS_SESSION_KEY, None)
            session[BANNERS_SESSION_KEY] = None
            if banners:
                context["banner"] = banners
        return context

    def form_valid(self, form):
        self.request.session[TIMER_SESSION_KEY] = datetime.datetime.utcnow().strftime(
            TIMER_FORMAT
        )
        uploaded_file = form.cleaned_data["banner_file"]
        horizontal_banners_per_row = form.cleaned_data["horizontal_banners_per_row"]
        vertical_banners_per_row = form.cleaned_data["vertical_banners_per_row"]
        try:
            gpx_files = extract_gpx_if_needed(uploaded_file)
            banners = self.parse_banners(gpx_files)
            self.put_banners_to_session(
                banners, horizontal_banners_per_row, vertical_banners_per_row
            )
        except exceptions.BaronBaleException as e:
            message_utils.add_error_message(self.request.session, str(e))
            logger.error("Error while parsing banners", e)
        except Exception:
            self.handle_error()
        finally:
            shutil.rmtree(
                os.path.join(tempfile.gettempdir(), uploaded_file.name),
                ignore_errors=True,
            )
        return super().form_valid(form)

    def handle_error(self):
        message_utils.add_error_message(
            self.request.session,
            _(
                "While parsing your banners an error occurred. "
                "The admin has been informed, please come back later."
            ),
        )
        error_text = traceback.format_exc()
        logger.error(error_text)
        mail.mail_admins("An error occurred while parsing banners!", error_text)

    def parse_banners(self, gpx_files):
        banners = banner_parser.collect_banner_urls(gpx_files, self.request.session)
        banners = banner_sorter.sort_banner(banners)
        return banners

    def put_banners_to_session(
        self, banners, horizontal_banners_per_row, vertical_banners_per_row
    ):
        joined_banners = join_banners(
            banners, horizontal_banners_per_row, vertical_banners_per_row
        )
        joined_banners += (
            "<p>"
            + _("The bannerlist was generated on")
            + ' <a href="https://baronbale.de/tools/gc/banner/">baronbale.de</a>'
            + "</p>"
        )
        self.request.session[BANNERS_SESSION_KEY] = joined_banners
        self.log_duration()

    def log_duration(self):
        start_time = datetime.datetime.strptime(
            self.request.session.pop(TIMER_SESSION_KEY), TIMER_FORMAT
        )
        now = datetime.datetime.utcnow()
        duration = now - start_time
        logger.info("Parsing banners took {}".format(duration))
