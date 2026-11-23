from django.shortcuts import render
from django.views.decorators.http import require_safe
from .pages import PAGES


@require_safe
def page(request, page_key):
    return render(request, 'pages/' + PAGES[page_key][1])
