from django.shortcuts import render, redirect
from practica2.models import Pages
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from sqlite3 import OperationalError
from urllib.parse import urljoin, urlsplit
from django.views.decorators.csrf import csrf_exempt
import urllib.parse

# Create your views here.

def get_absolute_url(self):

    if not (self.startswith("http://") or self.startswith("https://")):
        self = "http://" + self
    return self


def content(request, identificador):
    if request.method != "GET":
        return HttpResponse("Method not allowed", status=405)
    try:
        pag = Pages.objects.get(id = int(identificador))
        url = get_absolute_url(pag.page)
        print(url)
        return redirect(url)
    except ObjectDoesNotExist:
        return HttpResponse("Shortened URL doesn't exist", status=404)


def form():
    resp = "<html><body><h1>URL Shortener</h1>"
    resp += "<form action='/'' method='post'>"
    resp += "Site:<br> <input type='text' name = 'site' value='Google' required><br>"
    resp += "URL:<br> <input type='text' name = 'url' value='www.google.es' required><br>"
    resp += "<input type='submit' value='Submit'></form></body>"
    return(resp)

@csrf_exempt
def view_info(request):
    if request.method == "GET":
        resp = form()
        try:
            list_urls = Pages.objects.all()
            resp += "<p>Saved URLs:</p>"
            resp += "<ol>"
            #print(resp)
            for pag in list_urls:
                resp += '<li><a href="' + str(pag.id) + '">' + pag.name + "  (" + pag.page + ')</a></li>'
            resp += "</ol>"
            return HttpResponse(resp)
        except OperationalError:
            return HttpResponse("No content", status=404)

    if request.method == "POST" or request.method == "PUT":
        toParse = request.body.decode('utf-8')
        #newUrl = toParse.split('=')[1]
        name = urllib.parse.unquote_plus(toParse.split('&')[0].split('=')[1])
        url = urllib.parse.unquote_plus(toParse.split('&')[1].split('=')[1])
        #print("NAME: |" + name + "|    URL: |" + url + "|")
        url = get_absolute_url(url)
        try:
            pag = Pages.objects.get(page = url)
            resp = "URL already shortened: "
        except ObjectDoesNotExist:
            pag = Pages(name = name)
            #pag.name = newUrl
            pag.page = url
            pag.save()
            resp = "URL: "
        resp += "<a href=" + pag.page + ">" + pag.page + "</a>"
        resp += "</br>Shortened: <a href=/" + str(pag.id) + ">" + str(pag.id) + "</a> "
        resp += "</br><a href=/>Back</a> "
        return HttpResponse(resp)


def msg_error(request, msg):
    return HttpResponse(msg + ": content not valid", status=404)
