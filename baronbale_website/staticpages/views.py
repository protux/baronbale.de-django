from django.views.generic.base import TemplateView


class Contribute(TemplateView):
    template_name = 'staticpages/contribute.html'


class Imprint(TemplateView):
    template_name = 'staticpages/imprint.html'


class PrivacyPolicy(TemplateView):
    template_name = 'staticpages/privacy.html'


class Roadmap(TemplateView):
    template_name = 'staticpages/roadmap.html'
