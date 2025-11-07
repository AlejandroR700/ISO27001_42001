from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    company = forms.CharField(max_length=150, required=False)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)
