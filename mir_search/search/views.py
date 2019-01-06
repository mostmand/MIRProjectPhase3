from django.http import HttpResponse
import json
import searching


def search(request):
    if request.method == 'POST':
        dic = json.loads(request.body)
        searching.search.search(dic['mustArray'], dic['mustNotArray'], dic['shouldArray'])
        return HttpResponse('Salaam')
