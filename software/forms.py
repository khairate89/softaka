# software/forms.py

from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'content']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email (optional)'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Your Comment', 'rows': 4}),
        }
        labels = {
            'name': '',  # Empty label, as placeholder will guide
            'email': '',
            'content': '',
        }
        help_texts = {
            'name': None, # Remove default help text if any
            'email': None,
            'content': None,
        }