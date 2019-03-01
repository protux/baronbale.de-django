from django.utils.translation import ugettext as _

from baronbale_website.common import exceptions


class EmptyZipException(exceptions.BaronBaleException):
    def __str__(self):
        return _('The zip-file you provided was empty or did not contain any GPX-files.')
