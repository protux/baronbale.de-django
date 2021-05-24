from django.http.response import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import FormView

from baronbale_website.banner_parser.forms.upload_gpx_form import UploadGPXForm
from baronbale_website.banner_parser.models import BannerParserJob


class UploadListingFilesView(FormView):
    template_name = "banner_parser/upload_files.html"
    form_class = UploadGPXForm

    def form_valid(self, form) -> HttpResponseRedirect:
        uploaded_file = form.cleaned_data["banner_file"]
        horizontal_banners_per_row = form.cleaned_data["horizontal_banners_per_row"]
        vertical_banners_per_row = form.cleaned_data["vertical_banners_per_row"]

        banner_parser_job = BannerParserJob.objects.create(
            uploaded_file=uploaded_file,
            horizontal_banners_per_row=horizontal_banners_per_row,
            vertical_banners_per_row=vertical_banners_per_row,
        )

        return UploadListingFilesView.redirect_to_waiting_url(banner_parser_job)

    @staticmethod
    def redirect_to_waiting_url(
        banner_parser_job: BannerParserJob,
    ) -> HttpResponseRedirect:
        redirect_url: str = reverse_lazy(
            "banner_parser:queue", args=[banner_parser_job.ticket_id]
        )
        return HttpResponseRedirect(redirect_url)
