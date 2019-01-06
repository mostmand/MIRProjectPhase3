from django.http import HttpResponse
from django.shortcuts import render
import json


def search(request):
    if request.method == 'POST':
        dic = json.loads(request.body)
        print(dic['mustArray'])
        return HttpResponse('Salaam')
    else:
        return HttpResponse('Salaam')
