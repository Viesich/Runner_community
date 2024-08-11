from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms

from event.models import Runner, Event, Result, EventRegistration


class RunnerCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Runner
        fields = UserCreationForm.Meta.fields + ("first_name", "last_name", "date_of_birth", "gender", "phone_number")


class RunnerUpdateForm(forms.ModelForm):
    current_password = forms.CharField(
        widget=forms.PasswordInput,
        required=False,
        label="Current password",
    )

    new_password = forms.CharField(
        widget=forms.PasswordInput,
        required=False,
        label="New password",
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput,
        required=False,
        label="Confirm password",
    )

    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="Date of birth",
    )

    class Meta:
        model = Runner
        fields = ['username', 'first_name', 'last_name', 'date_of_birth', 'gender', 'phone_number']

    def clean(self):
        cleaned_data = super().clean()
        current_password = cleaned_data.get("current_password")
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        if new_password:
            if not current_password:
                raise forms.ValidationError("Please enter your current password to change your password.")

            if not self.instance.check_password(current_password):
                raise forms.ValidationError("The current password is incorrect.")

            if new_password != confirm_password:
                raise forms.ValidationError("Passwords do not match!")

        return cleaned_data

    def save(self, commit=True):
        runner = super().save(commit=False)
        new_password = self.cleaned_data.get("new_password")
        if new_password:
            runner.set_password(new_password)
        if commit:
            runner.save()
        return runner

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
