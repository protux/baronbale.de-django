from django.views.generic import TemplateView
from django.http.response import HttpResponseRedirect
from django.urls import reverse

from baronbale_website.banner_parser.models import BannerParserJob


class BannersReadyView(TemplateView):
    template_name = "banner_parser/banners_ready.html"

    def get(self, request, *args, **kwargs):
        banner_parser_job = self.fetch_banner_parser_job()
        if banner_parser_job.result is None:
            return HttpResponseRedirect(
                reverse("banner_parser:queue", args=[banner_parser_job.ticket_id])
            )

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        banner_parser_job = self.fetch_banner_parser_job()

        context_data["banner_parser_job"] = banner_parser_job
        return context_data

    def fetch_banner_parser_job(self):
        banner_parser_job = BannerParserJob.objects.get(
            ticket_id=self.get_ticket_id_from_path_param()
        )
        return banner_parser_job

    def get_ticket_id_from_path_param(self) -> str:
        return self.kwargs["ticket_id"]
