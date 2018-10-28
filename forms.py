# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms

class SearchForm(forms.Form):
    """ Handles the creation of a basic search form so users can type the words they would like to earch in the database.
    Edit the language field for adding more languages, just follow the examples provided."""

    search_term = forms.CharField(label="Search words")
    language = forms.ChoiceField(label="Language", choices=(("rus", "Russian"), ("eng", "English"), ("spa", "Spanish")), required=True)