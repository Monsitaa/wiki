from django.shortcuts import render
from . import util
from django.core.files.storage import default_storage
from markdown2 import Markdown
from django.http import Http404
import random


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entries(request, title):
    contenido = util.get_entry(title)

    if contenido is None:
        raise Http404

    return render(request, "encyclopedia/entries.html", {
        "title": title,
        "content": contenido
    })

def crearMD(request):

    if request.method == "POST":
        title = request.POST["title"]
        content = request.POST["content"]
        util.save_entry(title, content)
        return render(request, "encyclopedia/entries.html", {
            "title": title,
            "content": content
        })

    return render(request, "encyclopedia/crearMD.html")


def md_to_html(title):
    
    contenido = util.get_entry(title)
    markdowner = Markdown()

    if contenido == None:
        raise None

    return markdowner.convert(contenido)


def randomMD(request):
    entries = util.list_entries()

    randEntries = random.choice(entries)

    contenidoHTML = md_to_html(randEntries)

    return render(request, "encyclopedia/entries.html", {
        "title": randEntries,
        "content": contenidoHTML
    })

def search(request):
    query = request.GET['q']
    lista = util.list_entries()
    resultados = []
    for pagina in lista:
        if query.lower() in pagina.lower():
            resultados.append(pagina)
    
    resultados.sort()

    if len(resultados) == 1:
        return entries(request, resultados[0])
    elif len(resultados) > 1:
        return render(request, "encyclopedia/search.html", {
            "resultados": resultados,
            "query": query
        })
    else:
        return Http404