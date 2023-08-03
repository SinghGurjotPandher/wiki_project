from django.shortcuts import render
from . import util
from django.http import HttpResponse, HttpResponseRedirect
import markdown2
from django import forms
from django.forms import TextInput
from django.urls import reverse
import random

app_name = "encyclopedia"


class NewEntryForm(forms.Form):
    Title = forms.CharField(widget = forms.TextInput(attrs={'placeholder': 'Type your title here...', 'style': 'width: 300px','class': 'form-control'}))
    Content = forms.CharField(widget = forms.TextInput(attrs={'placeholder': 'Type your content here...', 'style': 'width: 500px', 'class': 'form-control'}))


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def get_entry(request):
    a = request.GET.get('q')
    if a in util.list_entries():
        return pullfile(request,a)
    else:
        all_match = []
        n = 0
        entries = util.list_entries()
        while n < len(util.list_entries()):
            if a in entries[n]:
                all_match.append(entries[n])
            n = n + 1
        return render(request, "encyclopedia/search_results.html",{
            "matches": all_match
        })


def new_entry(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["Title"]
            content = "<h1>" + title + "</h1>" + form.cleaned_data["Content"]
            if title in util.list_entries():
                return render(request, "encyclopedia/already_exists.html",{
                    "title": title
                })
            else:
                util.save_entry(title, content)
                return pullfile(request,title)
        else:
            return render(request, "encyclopedia/new_entry.html",{
                "form": NewEntryForm()
            })
    return render(request, "encyclopedia/new_entry.html", {
        "form": NewEntryForm()
    })

def pullfile(request, title):
    global global_var 
    global_var = title
    if title in util.list_entries():
        Func = open("encyclopedia/templates/encyclopedia/view_entry.html", "w")
        Func.write("{% extends 'encyclopedia/layout.html' %}")
        Func.write("{% block title %}")
        Func.write(title)
        Func.write(" Entry {% endblock %} {% block body %}")
        Func.write(markdown2.markdown(util.get_entry(title))) #Markdown to HTML Conversion
        Func.write("<br> <form action ='{% url 'edit_page' %}' method = 'post'>{% csrf_token %}<input type = 'submit' value = 'Edit'></form>{% endblock %}")
        Func.close()
        return render(request, "encyclopedia/view_entry.html")
        
    else:
        return render(request, "encyclopedia/error_msg.html", {
            "title": title
        })


def get_random(request):
    title = random.choice(util.list_entries())
    return pullfile(request,title)


def edit_page(request):
    return render(request, "encyclopedia/edit_entry.html",{
        "Global_Variable": global_var,
        "code": util.get_entry(global_var)
    })

def save_changes(request):
    code = request.GET.get("q")
    util.save_entry(global_var,code)
    return pullfile(request,global_var)