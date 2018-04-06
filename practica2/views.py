from django.shortcuts import render, redirect
from practica2.models import Pages
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from sqlite3 import OperationalError
from urllib.parse import urljoin, urlsplit
from django.views.decorators.csrf import csrf_exempt
import urllib.parse
#from .forms import PostForm

# Create your views here.

def get_absolute_url(self):
    # hacer un urlparse.join
    #return urljoin('http://www.', self.page)
    first = self.page[0:6]
    print("First: " + first)
    if (first == 'http:/') or (first == 'https:'):
        return self.page
    else:
        return "http://%s/" % self.page



def content(request, identificador):
    if request.method != "GET":
        return HttpResponse("Method not allowed", status=405)
    try:
        pag = Pages.objects.get(id = int(identificador))
        name_dom = get_absolute_url(pag)
        print(name_dom)
        return redirect(name_dom)
        #return redirect(pag.page)
    except ObjectDoesNotExist:
        return HttpResponse("Content not found", status=404)


def form():
    toReturn = "<html><body><h1>Introduzca URL a acortar: </h1>"
    toReturn += "<form action='/'' method='post'>"
    toReturn += "Nombre:<br> <input type='text' name = 'nombre' value='Google'><br>"
    toReturn += "URL:<br> <input type='text' name = 'url' value='google.es'><br>"
    toReturn += "<input type='submit' value='Submit'>"
    toReturn += "</form></body>"
    toReturn += "</br>URLs guardadas:"
    return(toReturn)

@csrf_exempt
def mostrar_info(request):
    if request.method == "GET":
        #return HttpResponse("Method not allowed", status=405)
        respuesta = form()
        try:
            lista = Pages.objects.all()
            respuesta += "<ol>"
            print(respuesta)
            for pag in lista:
                #respuesta += '<li><a href="' + str(pag.id) + '">' + pag.name + '</a>'
                respuesta += '<li><a href="' + str(pag.id) + '">' + pag.name + '</a>'
            respuesta += "</ol>"
            return HttpResponse(respuesta)
        except OperationalError:
            return HttpResponse("No content", status=404)

    if request.method == "POST" or request.method == "PUT":
        toParse = request.body.decode('utf-8')
        #newUrl = toParse.split('=')[1]
        name = urllib.parse.unquote_plus(toParse.split('&')[0])
        newUrl = urllib.parse.unquote_plus(toParse.split('&')[1])
        print("NAME: |" + name + "|    URL: |" + newUrl + "|")
        if not (newUrl.startswith("http://") or newUrl.startswith("https://")):
            newUrl = "http://" + newUrl
        try:
            pag = Pages.objects.get(page = newUrl)
            toReturn = "Su pagina ya estaba acortada, su pagina:"
        except ObjectDoesNotExist:
            pag = Pages(name = newUrl)
            #pag.name = newUrl
            pag.page = newUrl
            pag.save()
            toReturn = "Su pagina:"
        toReturn += "<a href=/" + pag.page + ">" + pag.page + "</a>"
        toReturn += "</br>Acortada es: <a href=/" + str(pag.id) + ">" + str(pag.id) + "</a> "
        return HttpResponse(toReturn)


def msg_error(request, msg):
    return HttpResponse(msg + ": content not found", status=404)
