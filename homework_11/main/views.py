from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse


def index(request):
    sliva_url = reverse('sliva')


    response_html = f"""
        <h1>Hello, Vasya!</h1>
        <br>
        <a href="{sliva_url}">Слива?</a>
        """
    return HttpResponse(response_html)

def index2(request):
    return render(request, "index.html")
