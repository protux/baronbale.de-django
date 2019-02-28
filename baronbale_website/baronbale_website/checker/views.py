from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse


def index(request):
    if request.method == 'POST':

        checker_code = request.POST.get('ccode')
        checker_code = checker_code.strip().lower()
        if checker_code == 'h gis fis e fis gis' or checker_code == "h'' gis'' fis'' e'' fis'' gis''" or checker_code == 'h" gis" fis" e" fis" gis"':
            return HttpResponseRedirect(reverse('checker:correct'))
        else:
            return HttpResponseRedirect(reverse('checker:incorrect'))

    return render(request, 'checker/checker.html')


def correct(request):
    return render(request, 'checker/correct.html')


def incorrect(request):
    return render(request, 'checker/incorrect.html')
