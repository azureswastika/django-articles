from django import forms
from django.contrib.auth import forms as auth

from .models import CustomUser


class UserCreationForm(auth.UserCreationForm):
    class Meta:
        model = CustomUser
        fields = "__all__"


class UserChangeForm(auth.UserChangeForm):
    class Meta:
        model = CustomUser
        fields = "__all__"


class FormModel(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "form-control"
            if field == 'email':
                self.fields[field].required = True
            if field == 'password1' or field == 'password2':
                self.fields[field].help_text = None


class LoginForm(auth.AuthenticationForm, FormModel):
    class Meta:
        model = CustomUser
        fields = ('username', 'password')


class RegisterForm(auth.UserCreationForm, FormModel):
    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'password1', 'password2')
