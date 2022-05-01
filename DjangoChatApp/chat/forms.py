from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from . models import RoomModel

class RoomCreateForm(forms.ModelForm):
    name = forms.CharField(
        widget = forms.TextInput(
            attrs = {
                'Placeholder' : 'E.g. Learn Django'
            }
        )
    )

    topic = forms.CharField(widget = forms.TextInput())

    description = forms.CharField(
        required=False,
        widget = forms.Textarea(
            attrs = {
                "Placeholder" : "Describe your group...",
            }
        )
    )

    class Meta:
        model = RoomModel
        fields = '__all__'
        exclude = [
            'host',
            'participants'
        ]

class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
        ]

