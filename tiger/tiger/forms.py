from django import forms
from django.forms.utils import ErrorList
from tiger import models

class SearchForm(forms.Form):
    keyword = forms.CharField()

class ContactForm(forms.ModelForm):
    company_id = forms.IntegerField()
    content = forms.CharField(widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        for field in self:
            field.field.widget.attrs['class']='form-control'

        self.fields['sender'].widget.attrs['placeholder'] = 'Please enter your name.'
        self.fields['title'].widget.attrs['placeholder'] = 'Please enter a title.'
        self.fields['mobile'].widget.attrs['placeholder'] = 'Please enter your contact number'
        self.fields['email'].widget.attrs['placeholder'] = 'Please enter your email'
        self.fields['content'].widget.attrs['placeholder'] = 'Please enter your name'
        self.fields['content'].required = False

    class Meta:
        model = models.Contact
        fields = ['sender', 'mobile', 'email', 'title', 'content']

    def clean_email(self):
        email = self.cleaned_data['email']
        if not "@" in email or not '.' in email:
            raise forms.ValidationError('Email is not valid')
        return email

    def on_frequent_submit(self):
        self.errors['remarks'] = ErrorList(['Sorry, Please submit another record in 5 minutes'])


class JoinUsForm(forms.ModelForm):
    remarks = forms.CharField(widget=forms.Textarea)
    def __init__(self, *args, **kwargs):
        super(JoinUsForm, self).__init__(*args, **kwargs)
        for field in self:
            field.field.widget.attrs['class']='form-control'

        self.fields['name'].widget.attrs['placeholder'] = 'Please input your name'
        self.fields['company'].widget.attrs['placeholder'] = 'Please input the company name'
        self.fields['mobile'].widget.attrs['placeholder'] = 'Please input the contact number'
        self.fields['email'].widget.attrs['placeholder'] = 'Please input the company email'
        self.fields['remarks'].widget.attrs['placeholder'] = 'Any other information you want us to know'
        self.fields['remarks'].required = False

    class Meta:
        model = models.Enquiry
        fields = ['name', 'company', 'mobile', 'email', 'region', 'remarks' ]

    def clean_email(self):
        email = self.cleaned_data['email']
        if not "@" in email or not '.' in email:
            raise forms.ValidationError('Email is not valid')
        return email

    def clean_mobile(self):
        tel = self.cleaned_data['mobile']
        if not tel.isdecimal():
            raise forms.ValidationError('Phone number must be all digits')
        return tel

    def on_frequent_submit(self):
        self.errors['remarks'] = ErrorList(['Sorry, Please submit another record in 5 minutes'])
