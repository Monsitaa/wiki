from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import redirect
from . import util
from django.core.files.storage import default_storage
from markdown2 import Markdown
from django.http import Http404
import random
import re

def contains_accented_characters(text):
    regex = r'[áéíóúÁÉÍÓÚüÜñÑ]'
    return bool(re.search(regex, text))

def is_valid_content(content):
    caracteres_disponibles = r'^[\s\S]+$'
    if contains_accented_characters(content):
        return False
    return re.match(caracteres_disponibles, content) is not None


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entries(request, title):
    html = md_to_html(title)

    if html is None:
        return render(request, "encyclopedia/404.html")
    else:
        try:
            return render(request, "encyclopedia/entries.html", {
                "title": title,
                "html": html
            })
        except Exception as e:
            print(e)
            return render(request, "encyclopedia/404.html")
def crearMD(request):

    if request.method == "POST":
        title = request.POST["title"]
        content = request.POST["content"]
        try: 
            if not is_valid_content(content):
                context = {
                    "title": title,
                    "content": content,
                    "error": True
                }
                return render(request, "encyclopedia/crearMD.html", context)
            else:
                util.save_entry(title, content)
                url = reverse("entries", args=[title])
                return redirect(url)
        except:
            pass
    return render(request, "encyclopedia/crearMD.html")


def md_to_html(entry):
    md = Markdown()
    content = util.get_entry(entry)
    if content is None:
        return None
    else:
        return md.convert(content)
    

def randomMD(request):
    pages = util.list_entries()
    random_page = pages[random.randint(0, (len(pages))-1)]
    url = reverse("entries", args=[random_page])
    return redirect(url)


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
        return render(request, "encyclopedia/404.html")
    
def edit(request, title):
    if request.method == "POST":
        contenido = request.POST["content"]
        title = request.POST["title"]
        try:

            if not is_valid_content(contenido):
                context = {
                    "title": title,
                    "content": contenido,
                    "error": True
                }

                return render(request, "encyclopedia/edit.html", context)

            util.save_entry(title, contenido)
            url = reverse("entries", args=[title])
            return redirect(url)
        except:
            pass
    else:
        content = util.get_entry(title)
        context = {
            "title": title,
            "content": content
        }
        return render(request, "encyclopedia/edit.html", context)
    

def delete(request, title):
   response = util.delete_entry(title)
   if response:
       url = reverse("index")
       return redirect(url + "?deleted=True")
   else:
        return render(request, "encyclopedia/404.html")
