from django.http.response import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import FormView

from baronbale_website.banner_parser.forms.add_email_address_form import (
    AddEmailAddressForm,
)
from baronbale_website.banner_parser.models import BannerParserJob


class WaitingQueueView(FormView):
    template_name = "banner_parser/wait_queue.html"
    form_class = AddEmailAddressForm

    def get(self, request, *args, **kwargs):
        self.banner_parser_job = self.fetch_banner_parser_job()
        if self.banner_parser_job.result is not None:
            return HttpResponseRedirect(
                reverse(
                    "banner_parser:show_banners",
                    args=[self.banner_parser_job.ticket_id],
                )
            )

        return super().get(request, *args, **kwargs)

    def fetch_banner_parser_job(self):
        banner_parser_job = BannerParserJob.objects.get(
            ticket_id=self.get_ticket_id_from_path_param()
        )
        return banner_parser_job

    def get_ticket_id_from_path_param(self) -> str:
        return self.kwargs["ticket_id"]

    def get_context_data(self, **kwargs) -> dict:
        context_data = super().get_context_data(**kwargs)
        context_data["ticket_id"] = self.banner_parser_job.ticket_id
        context_data["current_email"] = self.banner_parser_job.email_address_to_notify
        return context_data

    def form_valid(self, form: AddEmailAddressForm) -> HttpResponseRedirect:
        ticket_id: str = self.get_ticket_id_from_path_param()
        email_address: str = form.cleaned_data["email_address"]

        BannerParserJob.objects.filter(ticket_id=ticket_id).update(
            email_address_to_notify=email_address
        )

        return HttpResponseRedirect(reverse("banner_parser:queue", args=[ticket_id]))
