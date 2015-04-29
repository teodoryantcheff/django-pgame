from django.views.generic import TemplateView

__author__ = 'Jailbreaker'


class IndexView(TemplateView):
    template_name = 'index.html'