from django import forms
from .models import NetflixTitle

class NetflixTitleForm(forms.ModelForm):
    class Meta:
        model = NetflixTitle
        fields = '__all__'
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'cast': forms.Textarea(attrs={'rows': 3}),
            'date_added': forms.DateInput(attrs={'type': 'date'}),
        }