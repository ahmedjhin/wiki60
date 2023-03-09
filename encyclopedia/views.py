from django.shortcuts import render
import markdown
from . import util

def convert_md_to_html(title):
    content = util.get_entry(title)
    markdowner = markdown.Markdown()
    if content == None:
        return None
    else:
        return markdowner.convert(content)



def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request,title):
    html_content = convert_md_to_html(title)
    if html_content == None:
        return render(request,'encyclopedia/error.html',{
            'message':' This entry does not exist'
        })
    else:
        return render(request,'encyclopedia/entry.html',{
            'title': title,
            'content': html_content
        })
    
    
def search(request):
    if request.method == 'POST':
        entry_search = request.POST['q']
        html_contetn = convert_md_to_html(entry_search)
        if html_contetn is not None:
            return render(request, 'encyclopedia/entry.html',{
                'title': entry_search,
                'content': html_contetn
            })
        else:
            allEntries = util.list_entries()
            recommendation = []
            for entry in allEntries:
                if entry_search.lower() in entry.lower():
                    recommendation.append(entry)
            return render(request,'encyclopedia/search.html', {
                'recommendation': recommendation
            })



def new_page(request):
    if request.method == 'GET':
        return render(request,'encyclopedia/new_page.html',
                  {'title':'creat new page'})


def created_page(request):
    if request.method  == 'POST':
        page_title_is = request.POST['title']
        page_content = request.POST['content']
        md_content2 = util.save_entry(page_title_is,page_content)
        convertedHTML = util.get_entry(md_content2)
        html_content2 = convert_md_to_html(convertedHTML)
    
    return render(request,'encyclopedia/page_created.html',
                      {'content':html_content2,})
