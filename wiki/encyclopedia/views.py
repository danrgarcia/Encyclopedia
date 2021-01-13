from random import randrange

from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
import markdown2 as md

from . import util


def index(request, entries=None, header=None):
    if entries is None:
        entries = util.list_entries()
        header = "All entries"
    return render(request, "encyclopedia/index.html", {
        "entries": entries,
        "header": header
    })


def title(request, title):
    entry = util.get_entry(title)
    if entry is not None:
        info = md.markdown(entry)
    else:
        title = "Error"
        info = "<h1>Entry Not Found</h1><p>The entry you are looking for was not found.</p>"
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "entry": info
    })


def search(request):
    if request.method == "POST":
        form = request.POST
        title = form["q"]
        entry = util.get_entry(title)
        if entry is not None:
            return redirect(f'/wiki/{title}')
        else:
            matches = []
            entries = util.list_entries()
            for entry in entries:
                if title.upper() in entry.upper():
                    matches.append(entry)
            return render(request, "encyclopedia/index.html", {
                "entries": matches,
                "header": "Matching Results"
            })
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def newpage(request):
    if request.method == "POST":
        exists = False
        title = request.POST.get('title')
        content = request.POST.get('content')
        entries = util.list_entries()
        for entry in entries:
            if title.upper() == entry.upper():
                exists = True
        if exists:
            title = "Error"
            info = "<h1>Entry Already Exists</h1><p>There is already an entry for this item.</p>"
            return render(request, "encyclopedia/entry.html", {
                "title": title,
                "entry": info
            })
        else:
            util.save_entry(title, content)
            return redirect(f'/wiki/{title}')
    return render(request, "encyclopedia/edit.html", {
        "header": "Create New Page",
        "title": "",
        "content": ""
    })


def edit(request, title):
    if request.method == "POST":
        content = request.POST.get('content')
        util.save_entry(title, content)
        return redirect(f'/wiki/{title}')
    else:
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            "header": "Edit" + title,
            "title": title,
            "content": content
        })


def random(request):
    entries = util.list_entries()
    article_number = randrange(len(entries))
    title = entries[article_number]
    return redirect(f'/wiki/{title}')

