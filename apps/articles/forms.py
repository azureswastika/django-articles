from django import forms

from .models import Comment, Post


class FormModel(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "form-control"
            if field == "email":
                self.fields[field].required = True
            if field == "password1" or field == "password2":
                self.fields[field].help_text = None


class PostCreate(FormModel):
    class Meta:
        model = Post
        fields = ("text",)


class CommetModel(FormModel):
    class Meta:
        model = Comment
        fields = ["parent", "text"]
