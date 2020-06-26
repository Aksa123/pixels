from django.forms import ModelForm, CharField, Textarea, TextInput, ImageField, SelectMultiple, Select, FileInput
from photos.models import Photo, UserProfile, Tag


class PhotoForm(ModelForm):
    class Meta:
        model = Photo
        fields = ["photo", "name", "description", "user", "tag"]
        widgets = {
            "photo": FileInput(attrs={"class": "form-control"}),
            "name": TextInput(attrs={"class": "form-control"}),
            "description": Textarea(attrs={"class": "form-control" }),
            "tag": SelectMultiple(attrs={"class": "custom-select"}),
            "user": Select(attrs={"class": "form-control" })
        }


class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ["avatar", "name", "description", "slug"]
        widgets = {
            "avatar": FileInput(attrs={"class": "form-control"}),
            "name": TextInput(attrs={"class": "form-control"}),
            "description": Textarea(attrs={"class": "form-control"}),
            "slug": TextInput(attrs={"class": "form-control"})
        }


class TagForm(ModelForm):
    class Meta:
        model = Tag
        fields = ["name"]
        widgets = {
            "name": TextInput(attrs={"class": "form-control"})
        }