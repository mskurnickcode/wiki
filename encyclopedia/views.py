from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from markdown2 import markdown
from django import forms
from . import util
from random import randint

class SearchForm(forms.Form):
    search = forms.CharField(label="Search", required= False)
    widget = forms.Textarea(attrs={'placeholder':'Search Encyclopedia'})

class NewEntryForm(forms.Form):
    title = forms.CharField(label="Title", required=True)
    content = forms.CharField(label="content", widget=forms.Textarea)

class EditForm(forms.Form):
    title = forms.CharField(label="")
    content = forms.CharField(label="", widget=forms.Textarea)



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
        return render(request, "encyclopedia/error.html", {
        "error": "Page Does Not Exist",
        "text": "Please create a page for new users"
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

def edit(request, entry):
    if request.method == 'GET':
        page = util.get_entry(entry)

        information  = {
            'edit': EditForm(initial={'content': page, 'title':entry}),
        }
        return render(request, "encyclopedia/edit.html", information)

    

def save_edit(request, entry):
    if request.method == 'POST':
        print("post valid")
        form = EditForm(request.POST)
        print("form recieved")
        content = request.POST.get("content", "").strip()
        title = request.POST.get("title", "").strip()
        print(content)
        print(title)

        util.save_entry(title, content)
        entry = util.get_entry(title)
        page = markdown(entry)
        return render(request, "encyclopedia/entry.html", {
        "entry": title,
        "content": page
        })

    else:
        return render(request, "encyclopedia/error.html", {
                    "error": "Error",
                    "text": "Your Submission Couldn't be Saved.  Please go back."
                })

def random(request):
    entries = util.list_entries()
    rangeInt = len(entries)-1
    number = randint(0,rangeInt)
    print(entries[number])
    randEntry = entries[number]
    entry = util.get_entry(randEntry)
    page = markdown(entry)
    return render(request, "encyclopedia/entry.html", {
    "entry": randEntry,
    "content": page
    })
    











