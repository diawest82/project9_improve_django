from django import forms
from django.forms.extras.widgets import SelectDateWidget

from .models import Menu, Item, Ingredient


class MenuForm(forms.ModelForm):
    items = forms.ModelMultipleChoiceField(queryset=Item.objects.all(), widget=forms.SelectMultiple())
    expiration_date = forms.DateTimeField(
        input_formats=['%Y-%m-%d', '%m/%d/%Y', '%m/%d/%y'],
        widget=forms.SelectDateWidget(years=range(2017, 2021))
    )

    class Meta:
        model = Menu
        exclude = ('created_date',)

    def clean(self):
        data = self.cleaned_data
        season = data.get('season')

        if not season:
            raise forms.ValidationError(
                "A season name is required"
            )
        return data


class ChangeMenuForm(forms.ModelForm):
    items = forms.ModelMultipleChoiceField(queryset=Item.objects.all(), widget=forms.SelectMultiple())
    expiration_date = forms.DateTimeField(
        input_formats=['%Y-%m-%d', '%m/%d/%Y', '%m/%d/%y'],
        widget=forms.SelectDateWidget(years=range(2017, 2021))
    )

    class Meta:
        model = Menu
        exclude = ('created_date',)

    def clean(self):
        data = self.cleaned_data
        season = data.get('season')

        if not season:
            raise forms.ValidationError(
                "A season name is required"
            )
        return data
