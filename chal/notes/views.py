from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Note
from . import forms
from django.conf import settings
from django.urls import reverse
from django.template import engines
import urllib
import html
import re

def sanitize_input(input_str):
    sanitized_input = re.sub(r'{.*?}', '', input_str)
    return urllib.parse.unquote(sanitized_input)

def is_ssti_vulnerable(input_str):
    ssti_indicators = ['{{', '}}']
    for indicator in ssti_indicators:
        if indicator in input_str:
            return True
    return False

def say_hello(request):
    return redirect(reverse('notes:make_note'))

def show_notes(request):
    alias = request.GET.get('alias') or 'User'  
    alias = sanitize_input(alias)

    notes = Note.objects.all()

    engine = engines['django']

    template_string = f"""
    <html>
    <head>
        <title>Notes</title>
        <style>
            body {{
                font-family:'Roboto Mono',monospace;
                margin: 0;
                padding: 0;
                background-color: #f0f5ff;
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
            }}
            .delete-notes-form {{
                text-align: center;
                margin-top: 20px;
            }}

            .delete-notes-btn {{
                background-color: #007bff;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                cursor: pointer;
                font-size: 16px;
            }}

            .delete-notes-btn:hover {{
                background-color: #D73817;
            }}

            .container {{
                max-width: 800px;
                width: 100%;
                padding: 20px;
                background-color: #fff;
                border-radius: 10px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }}
            h1 {{
                text-align: center;
                color: #000080;
                margin-bottom: 20px;
            }}
            .alias {{
                background-color: #f8f8ff;
                border-radius: 10px;
                padding: 20px;
                margin-bottom: 20px;
                box-shadow: 0 3px 10px rgba(0, 0, 0, 0.1);
            }}
            .alias h2 {{
                color: #000080;
                margin-top: 0;
                margin-bottom: 10px;
            }}
            .alias p {{
                color: #556B2F;
                margin-top: 0;
            }}
            .notes-container {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 20px;
            }}
            .note {{
                background-color: #f8f8ff;
                border-radius: 10px;
                padding: 20px;
                box-shadow: 0 3px 10px rgba(0, 0, 0, 0.1);
            }}
            .note h3 {{
                color: #000080;
                margin-top: 0;
                margin-bottom: 10px;
            }}
            .note p {{
                color: #556B2F;
                margin-top: 0;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Notes</h1>
            <div class="alias">
                <h2>Hello, {alias}!!</p>
            </div>
            <div class="notes-container">
            <div class="note">
            <h3>Welcome to my notes app!</h3>
            <p>You can write your secrets here, or maybe leak some..&#128520;</p></div>
             <div class="note">
            <h3>Try to get the secrets</h3>
            <p>The admin seems to left his secrets unprotected, maybe you can get 'em!</p>
        
        </div>
            """
    
    for note in notes:
        template_string += f"""
        <div class="note">
            <h3>{html.escape(note.title)}</h3>
            <p>{html.escape(note.body)}</p>
        </div>
        """

    template_string += """    </div><form class="delete-notes-form" action="{% url 'notes:delete_notes' %}" method="post">
    {% csrf_token %}
    <button class="delete-notes-btn" type="submit">Delete All Notes</button>
</form>


        
        </div>
    </body>
    </html>
    """

    rendered_template = engine.from_string(template_string).render({'notes': notes, 'alias': alias, "settings": settings}, request)
    return HttpResponse(rendered_template)

def make_note(request):
    if request.method == "POST":
        form = forms.NoteForm(request.POST)
        notes = Note.objects.all()
        alias = request.POST.get('alias', None)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            body = form.cleaned_data.get('body')
            if is_ssti_vulnerable(title) or is_ssti_vulnerable(body):
                # If SSTI vulnerability found, return an error response
                return HttpResponse("Error: SSTI detected.", status=400)
            else:
                form.save()
                return redirect('notes:show_notes') + f'?alias={alias}'
    else:
        form = forms.NoteForm()
    return render(request, 'index.html', {'form': form})

def delete_notes(request):
    Note.objects.all().delete()
    return redirect('notes:show_notes')
