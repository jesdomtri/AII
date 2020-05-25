# -*- encoding: utf-8 -*-
from django import forms

class UserForm(forms.Form):
    id = forms.CharField(label='User ID')
    
class IsbnForm(forms.Form):
    id = forms.CharField(label='ISBN ID')