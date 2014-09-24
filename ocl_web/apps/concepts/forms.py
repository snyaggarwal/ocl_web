# -*- coding: utf-8 -*-
"""
    Forms for concepts.
"""
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse

from django import forms
from django.forms.formsets import formset_factory

from libs.ocl import OCLapi
from apps.core import LOCALE_LIST

class ConceptCreateForm(forms.Form):
    """
        Concept edit form
    """
    required_css_class = 'required'

    concept_id = forms.CharField(max_length=30, label=_('Concept ID'), required=True)
    concept_class = forms.CharField(max_length=30, label=_('Concept Class'), required=True)
    datatype = forms.CharField(max_length=30, label=_('Datatype'), required=False)
    name = forms.CharField(max_length=30, label=_('Name'), required=True)
    locale = forms.ChoiceField(choices=LOCALE_LIST, label=_('Locale'),  required=True)
    preferred_locale = forms.BooleanField(label=_('Preferred Locale'), required=False, initial=False)

    def clean_concept_id(self):
        """ concept ID must be unique """
        concept_id = self.cleaned_data['concept_id']
        source = self.initial['source']
        request = self.initial['request']
        api = OCLapi(request, debug=True)
        result = api.get('orgs', source['owner'], 'sources', source['id'], 'concepts', concept_id)
        if result.status_code == 200:
            raise forms.ValidationError(_('This Concept ID is already used.'))
        return concept_id


class ConceptNameForm(forms.Form):
    """
        Form for a single concept name.
    """
    required_css_class = 'required'


    name = forms.CharField(max_length=30, label=_('Name'), required=True)
    locale = forms.CharField(max_length=30, label=_('Locale'),  required=True)
    preferred_locale = forms.BooleanField(label=_('Preferred Locale'), required=False, initial=False)
    name_type = forms.CharField(max_length=30, label=_('Name Datatype'), required=False)

ConceptNameFormSet = formset_factory(ConceptNameForm, extra=3)