from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms

from event.models import Runner, Event, Result, EventRegistration


class RunnerCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Runner
        fields = UserCreationForm.Meta.fields + ("first_name", "last_name", "date_of_birth", "gender", "phone_number")


class RunnerUpdateForm(forms.ModelForm):
    class Meta:
        model = Runner
        fields = ['first_name', 'last_name', 'date_of_birth', 'gender', 'phone_number']
# class BookForm(forms.ModelForm):
#     authors = forms.ModelMultipleChoiceField(
#         queryset=get_user_model().objects.all(),
#         widget=forms.CheckboxSelectMultiple(),
#         required=False,
#     )
#
#     class Meta:
#         model = Book
#         fields = "__all__"
#
#
# class BookSearchForm(forms.Form):
#     title = forms.CharField(
#         max_length=100,
#         required=True,
#         label="",
#         widget=forms.TextInput(
#             attrs={"placeholder": "Title"}),
#     )
