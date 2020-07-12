from django import forms

from places.models import Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["title", "body", "rating"]


class RestaurantForm(forms.Form):
    category = forms.CharField(help_text="Enter search pattern", required=False)
    name = forms.CharField(help_text="Enter search pattern", required=False)
    min_party = forms.IntegerField(help_text="Enter integer", required=False)
    max_party = forms.IntegerField(help_text="Enter integer", required=False)
