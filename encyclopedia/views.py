from django.shortcuts import render, redirect
import markdown2
import random

from . import util

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def content(request, title):
    content = util.get_entry(title)
    
    if content:
        return render(request, "encyclopedia/title.html", {
            "content": markdown2.markdown(content),
            "title": title
        })
    
    return render(request, "encyclopedia/apology.html", {
        "message": f"{title} page do not exists."
    })

def search(request):
    title = request.GET.get("q", "").strip()

    if not title:
        return render(request, "encyclopedia/apology.html", {
            "message": "Search field cannot be empty."
        })
    
    if util.get_entry(title):
        return redirect("encyclopedia:content", title=title)
    
    matches = [entry for entry in util.list_entries() if title.lower() in entry.lower()]
    if matches:
        return render(request, "encyclopedia/search.html", {
            "matches": matches,
            "title": title
        })
        
    return render(request, "encyclopedia/apology.html", {
        "message": "No match found."
    })

def new(request):
    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        content = request.POST.get("content", "").strip()

        if not title or not content:
            return render(request, "encyclopedia/apology.html", {
                "message": "Please provide both title and content."
            })
        
        for entry in util.list_entries():
            if title.lower() == entry.lower():
                return render(request, "encyclopedia/apology.html", {
                    "message": "Title already exists."
                })
            
        util.save_entry(title, content)
        return redirect("encyclopedia:content", title=title)
    
    return render(request, "encyclopedia/new.html")
    
def edit(request, title):
    if request.method == "POST":
        content = request.POST.get("content", "").strip()

        if not content:
            return render(request, "encyclopedia/apology.html", {
                "message": "Content cannot be empty."
            })
        
        util.save_entry(title, content)
        return redirect("encyclopedia:content", title=title)
    
    content = util.get_entry(title)

    if not content:
        return render(request, "encyclopedia/apology.html", {
            "message": f"No entry found with the title: {title}."
        })

    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "content": content
    })
    
def random_page(request):
    titles = util.list_entries()

    if titles:
        title = random.choice(titles)
        return redirect("encyclopedia:content", title=title)
    
    return render(request, "encyclopedia/apology.html", {
        "message": "No titles available."
    })
