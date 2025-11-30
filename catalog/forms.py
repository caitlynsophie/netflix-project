from .models import NetflixTitle, Review
from django import forms

class NetflixTitleForm(forms.ModelForm):
    class Meta:
        model = NetflixTitle
        fields = [
            'title_type',
            'title',
            'director',
            'cast',
            'country',
            'date_added',
            'release_year',
            'rating',
            'duration',
            'genres',
            'description',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'cast': forms.Textarea(attrs={'rows': 3}),
            'date_added': forms.DateInput(attrs={'type': 'date'}),
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'review_text', 'date_watched']
        widgets = {
            'review_text': forms.Textarea(attrs={'rows': 3}),
            'date_watched': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_rating(self):
        rating = self.cleaned_data['rating']
        if not (1 <= rating <= 5):
            raise forms.ValidationError("Rating must be between 1 and 5.") # Rating validation
        return rating