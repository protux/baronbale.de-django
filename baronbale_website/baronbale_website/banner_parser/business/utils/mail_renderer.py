from django.template import (
    Context,
    Engine,
    Template,
)

from baronbale_website.banner_parser.models import BannerParserJob


def render_mail_body(banner_parser_jon: BannerParserJob) -> str:
    template: Template = Engine.get_default().get_template(
        "banner_parser/email/job_finished.txt"
    )
    return template.render(Context({"ticket_id": banner_parser_jon.ticket_id}))
