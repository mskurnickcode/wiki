from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from markdown2 import markdown
from django import forms
from . import util

class SearchForm(forms.Form):
    search = forms.CharField(label="Search", required= False)
    widget = forms.TextInput(attrs={'placeholder':'Search Encyclopedia'})

class NewEntryForm(forms.Form):
    title = forms.CharField(label="Title", required=True)
    content = forms.CharField(widget=forms.Textarea)


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

def new(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]

            entries = util.list_entries()
            if title in entries:
                return render(request, "encyclopedia/error.html", {
                    "error": "Entry Exists",
                    "text": "Please edit the entry through it's page"
                })

            else:
                markdown_title = "#" + title
                new_content = markdown_title + "\n" + content
                util.save_entry(title, new_content)
                entry = util.get_entry(title)
                page = markdown(entry)
                return render(request, "encyclopedia/entry.html", {
                "entry": title,
                "content": page
                })

    else:
        return render(request, "encyclopedia/new.html", {
            "form": NewEntryForm()
        })



