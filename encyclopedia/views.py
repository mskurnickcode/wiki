from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from markdown2 import markdown
from django import forms
from . import util

class SearchForm(forms.Form):
    search = forms.CharField(label="Search", required= False)
    widget = forms.TextInput(attrs={'placeholder':'Search Encyclopedia'})

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry):
    page = util.get_entry(entry)
    if page is None:
        return render(request, "encyclopedia/entry.html", {
        "entry": "Does not exist"
    })
    
    page = markdown(page)
    return render(request, "encyclopedia/entry.html", {
        "entry": entry,
        "content": page
    })

def search(request):
    query = request.GET['q']
    if util.get_entry(query):
        return HttpResponseRedirect(reverse("wiki:entry", args=(query,)))

    else:
        return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })



