from django import forms

class NameForm(forms.Form):
    user_name = forms.CharField(label="Your Name", max_length=100)

class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea, label='Message')
    name = forms.CharField(max_length=25, label='Name')
    sender = forms.EmailField()