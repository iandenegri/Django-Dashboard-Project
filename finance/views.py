from django.shortcuts import render
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt


from .models import Company
from .as_dash import dispatcher

from rest_framework.response import Response
from rest_framework.views import APIView

# Create your views here.

def company_article_list(request):
    return render(request, "finance/plotly.html", {})

class ChartData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        article_dict = dict()
        for company in Company.objects.all():
            if company.articles > 0:
                # This is in theory really simple but referring to itself like this is kind of confusing...
                # Create key:value pairs where the key is the company that's being iterated through and the \
                # value is all the articles belonging to that company
                article_dict[company.name] = company.articles
        
        # Sort them from least to greatest. Not really necessary unless you want it to look nice..
        print(article_dict)
        article_dict = sorted(article_dict.items(),key=lambda x: x[1])
        print(article_dict)
        article_dict = dict(article_dict)
        print(article_dict)

        data = {
            "article_labels":article_dict.keys(),
            "article_data":article_dict.values(),
        }

        return Response(data)


### dash ###

def dash(request, **kwargs):
    return HttpResponse(dispatcher(request))


@csrf_exempt
def dash_ajax(request):
    return HttpResponse(dispatcher(request), content_type='application/json')