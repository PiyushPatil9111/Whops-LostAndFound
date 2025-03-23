from django import forms
from .models import Item, Profile

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['title', 'description', 'location', 'date', 'image', 'status']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['mobile_number', 'address', 'email']
    def save(self, commit=True):
        profile = super().save(commit=False)
        if profile.email:
            # Update the email field in the User model
            profile.user.email = profile.email
            profile.user.save()
        if commit:
            profile.save()
        return profile