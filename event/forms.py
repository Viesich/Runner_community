from django.contrib.auth.forms import UserCreationForm
from django import forms

from event.models import Runner, Event, Result, Registration


class RunnerCreationForm(UserCreationForm):
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="Date of birth",
    )

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


class EventCreationForm(forms.ModelForm):
    start_datetime = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        label="Start date and time",
    )

    location = forms.CharField(
        label="City, street, starting point",
    )

    class Meta:
        model = Event
        fields = [
            'name',
            'start_datetime',
            'location',
            'distances',
            'description',
            'event_type',
            'organiser',
            'is_active'
        ]


class EventSearchForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={"placeholder": "Name"}),
    )
    location = forms.CharField(
        max_length=100,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={"placeholder": "Location"}),
    )


# class RegistrationCreateForm(forms.ModelForm):
#     class Meta:
#         model = Registration
#         fields = ['event', 'runner', 'distance']
#
