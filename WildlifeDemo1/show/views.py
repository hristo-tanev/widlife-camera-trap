import os
from datetime import datetime
from django.shortcuts import render, loader
from django.http import HttpResponse

from models import Bird

day = None
PATH = os.path.dirname(__file__) + '/static/show/images/'


def formatDates():
    originalDates = os.listdir(PATH)
    newDates = []
    for date in originalDates:
        dmy = date.split(".")
        newDates.append(str(dmy[0] + '/' + dmy[1] + '/' + dmy[2]))

    return newDates


def index(request):
    global day
    days = sorted(formatDates(), key=lambda date: (
        int(date.split("/")[2]), int(date.split("/")[1]), int(date.split("/")[0])))
    context = {
        'first': days[0],
        'days': days[1:],
    }

    if request.method == 'POST':
        try:
            day = request.POST.getlist('day')[0]
        except:
            print('')

    if day != None:
        day = day.replace('/', '.')
        daySplit = [x.strip('0') for x in day.split('.')]
        context['selected_day'] = day
        context['previous'] = Bird.objects.filter(
            daym=daySplit[0], month=daySplit[1], year=daySplit[2])

    template = loader.get_template("show/index.html")
    return HttpResponse(template.render(context, request))
