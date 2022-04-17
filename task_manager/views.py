from django.http import HttpResponse
from django.utils.translation import gettext as _


def hello(request):
    text = _('Привет, Хекслет!')
    return HttpResponse(text)
