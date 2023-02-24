from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from markdown2 import Markdown
a = Markdown()
from django import forms
from . import util
import random



def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
	entry1 = util.get_entry(title)
	entries = util.list_entries()
	if title in entries:
		return render(request, "encyclopedia/entry.html", {
			"entry": a.convert(entry1),
			"entry_title": title
		})
	else:
		return render(request, "encyclopedia/NoEntry.html", {
				"entry_title": title
		})


def search(request):
    input = request.GET.get('q')
    entries = util.list_entries()

    if util.get_entry(input)!= None:
        return HttpResponseRedirect(reverse("entry", kwargs={'title': input }))
    else:
        subString = []
        for entry in entries:
            if input.lower() in entry.lower():
                subString.append(entry)

        return render(request, "encyclopedia/search.html", {
        "entries": subString,
        "input": input
    })

class NewForm(forms.Form):
	title = forms.CharField(label = "Title", widget = forms.TextInput(attrs = {'class' : 'form-control col-md-7 col-lg-7'}))
	text = forms.CharField(widget = forms.Textarea(attrs={'class' : 'form-control col-md-7 col-lg-7', 'rows' : 10}))

class Edit(forms.Form):
	text = forms.CharField(widget = forms.Textarea(attrs={'class' : 'form-control col-md-7 col-lg-7', 'rows' : 10}))


def newForm(request):
	if request.method == "POST":
		form = NewForm(request.POST)
		if form.is_valid():
			title = form.cleaned_data["title"]
			text = form.cleaned_data["text"]
			text2 = util.get_entry(title)
			if text2 is None:
				util.save_entry(title, text)
				return HttpResponseRedirect(reverse("entry", kwargs={'title': title}))
			else:
				return render(request, "encyclopedia/error.html", {
				"form": form,
				"entry_title": title
				})

		else:
		   	return render(request, "encyclopedia/newForm.html", {
		"form": form
		})

	else:
		return render(request, "encyclopedia/newForm.html", {

	"form": NewForm()
	})

def editPage(request, title):

    if request.method == "GET":
        text = util.get_entry(title)

        if text is None:
            util.save_entry(title, text)
        return render(request, "encyclopedia/editPage.html", {
          "title": title,
          "EditForm": Edit(initial={'text':text}),
          "NewForm": NewForm()
        })

    elif request.method == "POST":
        form = Edit(request.POST)

        if form.is_valid():
          text = form.cleaned_data['text']
          util.save_entry(title, text)
          return redirect(reverse('entry', args=[title]))




def random_seite(request):
    seiten = util.list_entries()
    seite = random.choice(seiten)

    return redirect(reverse('entry', args=[seite]))
