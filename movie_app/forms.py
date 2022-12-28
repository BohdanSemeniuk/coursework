from django import forms

from .models import Reviews


class ReviewForm(forms.ModelForm):

    class Meta:
        model = Reviews
        fields = ('text', )
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'id': 'contact-comment'})
        }
