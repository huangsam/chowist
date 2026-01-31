from django import forms
from django.core.exceptions import ValidationError

from places.models import Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["title", "body", "rating"]

    def clean_rating(self):
        rating = self.cleaned_data.get("rating")
        if rating is not None and (rating < 1 or rating > 5):
            raise ValidationError("Rating must be between 1 and 5.")
        return rating

    def clean_title(self):
        title = self.cleaned_data.get("title")
        if title and len(title.strip()) < 3:
            raise ValidationError("Title must be at least 3 characters long.")
        return title

    def clean_body(self):
        body = self.cleaned_data.get("body")
        if body and len(body.strip()) < 10:
            raise ValidationError("Review body must be at least 10 characters long.")
        return body


class RestaurantForm(forms.Form):
    category = forms.CharField(help_text="Enter search pattern", required=False)
    name = forms.CharField(help_text="Enter search pattern", required=False)
    min_party = forms.IntegerField(help_text="Enter integer", required=False, min_value=1)
    max_party = forms.IntegerField(help_text="Enter integer", required=False, min_value=1)

    def clean_min_party(self):
        min_party = self.cleaned_data.get("min_party")
        if min_party is not None and min_party < 1:
            raise ValidationError("Minimum party size must be at least 1.")
        return min_party

    def clean_max_party(self):
        max_party = self.cleaned_data.get("max_party")
        if max_party is not None and max_party < 1:
            raise ValidationError("Maximum party size must be at least 1.")
        return max_party

    def clean(self):
        cleaned_data = super().clean()
        min_party = cleaned_data.get("min_party")
        max_party = cleaned_data.get("max_party")

        if min_party and max_party and min_party > max_party:
            raise ValidationError("Minimum party size cannot exceed maximum party size.")

        return cleaned_data
