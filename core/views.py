from django.shortcuts import HttpResponse


def root(request):
    """show api is working with this view"""
    return HttpResponse("Api working. All systems running")
