from django.core.management.base import BaseCommand

from baronbale_website.banner_parser.business import parse_banner_command_executor


class Command(BaseCommand):
    help = "Looks for queued banner parse jobs and searches them for banners"

    def handle(self, *args, **options) -> None:
        parse_banner_command_executor.parse_banners()
