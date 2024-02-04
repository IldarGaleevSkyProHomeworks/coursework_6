from django.template import RequestContext
from django.shortcuts import render


def e_handler403(request, exception):
    return render(request, 'shared/errors/403.html', status=403)


def e_handler404(request, exception):
    return render(request, 'shared/errors/404.html', status=404)
