from django import forms
from tiger import models

class ContactForm(forms.ModelForm):
    company_id = forms.IntegerField()
    class Meta:
        model = models.Contact
        fields = ['sender', 'mobile', 'email', 'title', 'content']

