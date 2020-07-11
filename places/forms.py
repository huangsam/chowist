from django import forms

from places.models import Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["title", "body", "rating"]
