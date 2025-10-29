from django import forms
from .models import Event, Participant, Category


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ["name", "description", "date", "time", "location", "category"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "placeholder": "Event name",
                    "class": "w-full border rounded px-3 py-2",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "placeholder": "Description",
                    "class": "w-full border rounded px-3 py-2",
                    "rows": 3,
                }
            ),
            "date": forms.DateInput(
                attrs={"type": "date", "class": "w-full border rounded px-3 py-2"}
            ),
            "time": forms.TimeInput(
                attrs={"type": "time", "class": "w-full border rounded px-3 py-2"}
            ),
            "location": forms.TextInput(
                attrs={
                    "placeholder": "Location",
                    "class": "w-full border rounded px-3 py-2",
                }
            ),
            "category": forms.Select(
                attrs={"class": "w-full border rounded px-3 py-2"}
            ),
        }


class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ["name", "email", "events"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "placeholder": "Name",
                    "class": "w-full border rounded px-3 py-2",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "placeholder": "Email",
                    "class": "w-full border rounded px-3 py-2",
                }
            ),
            "events": forms.SelectMultiple(
                attrs={"class": "w-full border rounded px-3 py-2"}
            ),
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "description"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "placeholder": "Category name",
                    "class": "w-full border rounded px-3 py-2",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "placeholder": "Description",
                    "class": "w-full border rounded px-3 py-2",
                    "rows": 3,
                }
            ),
        }
