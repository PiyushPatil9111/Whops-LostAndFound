from django import forms
from .models import Item, Profile

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['title', 'description', 'location', 'date', 'image', 'status']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['mobile_number', 'address']