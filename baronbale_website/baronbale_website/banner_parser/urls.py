from django.urls import path

from baronbale_website.banner_parser.views.upload_listing_files_view import (
    UploadListingFilesView,
)
from baronbale_website.banner_parser.views.waiting_queue_view import WaitingQueueView
from baronbale_website.banner_parser.views.banners_ready_view import BannersReadyView

app_name = "banner_parser"
urlpatterns = [
    path("", UploadListingFilesView.as_view(), name="upload_listing_files"),
    path("queue/<str:ticket_id>", WaitingQueueView.as_view(), name="queue"),
    path("show/<str:ticket_id>", BannersReadyView.as_view(), name="show_banners"),
]
