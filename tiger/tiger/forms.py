from django import forms
from tiger import models

class SearchForm(forms.Form):
    keyword = forms.CharField()

class ContactForm(forms.ModelForm):
    company_id = forms.IntegerField()
    class Meta:
        model = models.Contact
        fields = ['sender', 'mobile', 'email', 'title', 'content']

