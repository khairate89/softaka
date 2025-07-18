# software/forms.py

from django import forms
from .models import Comment
from django.utils.translation import gettext_lazy as _

class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Your Name')}),
        help_text=_("Please enter your full name.")
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': _('Your Email')}),
        help_text=_("We'll use this to reply to you.")
    )
    subject = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Subject')}),
        help_text=_("Briefly describe the purpose of your message.")
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': _('Your Message')}),
        help_text=_("Please provide as much detail as possible.")
    )

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'content']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Name',
                'autocomplete': 'name',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Email (optional)',
                'autocomplete': 'email',
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Your Comment',
                'rows': 4,
                'autocomplete': 'off',  # Optional or use 'on'
            }),
        }
        labels = {
            'name': '',
            'email': '',
            'content': '',
        }
        help_texts = {
            'name': None,
            'email': None,
            'content': None,
        }
