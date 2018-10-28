# -*- coding: utf-8 -*-
"""This small application will search sentences in the database. Database has been filled previously with data from the Tatoeba project."""
from __future__ import unicode_literals
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import phrase
from .forms import SearchForm

# Language dictionary. Keys should be language codes (ISO 639-3) (eng for english, spa for  spanish, rus for russian and so on)
# value should be the language as will be used to generate text to speech responses in the response.js library
# (English, Russian, Spanish Latin American, etc).
# Obviously, there should be phrases already loaded in the database for all of the following languages.
languages = dict(eng="English", rus="Russian", spa="Spanish Latin American")

def index(request):
    """ Index method. From this method the search of sentences is processed, though if user didn't want to search anything we will show some informative page here."""
    will_search = False
    search_term = request.GET.get("search_term")
    language = request.GET.get("language")
    if search_term != None:
        will_search = True
    # prefill the form with search_term and language just in case these values are different than None.
    # It is useful so users will see the same data in their form even when the page has been reloaded due to a submit.
    # if these values are None, the form will be blank.
    search_form = SearchForm(initial=dict(search_term=search_term, language=language))
    if will_search == True:
        # ToDo: perhaps should I look to implement an "exact" search expresion for search_term here?
        posts = phrase.objects.filter(phrase__contains=search_term, language__exact=language)
        paginator = Paginator(posts, 100)
        # get page number from request args. If there is no page argument, then set page to 1.
        page = request.GET.get('page')
        if page == None: page = 1
        posts = paginator.page(page)
        # Add extra arguments (search_term and language) so other links will be loaded correctly in the paginator.
        extra_params = ""
        if search_term != None:
            extra_params = "&search_term={0}&language={1}".format(search_term, language)
    if will_search:
        return render(request, 'sentence_finder/index.html', dict(posts=posts, search_form=search_form, extra_params=extra_params, lang=languages.get(language)))
    else:
        return render(request, 'sentence_finder/index.html', dict(total=phrase.objects.count(), search_form=search_form))