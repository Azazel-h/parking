from django.shortcuts import render


def index_page(request) -> render:
    return render(request, "pages/index.html")
