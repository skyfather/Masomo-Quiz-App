from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.db import transaction

from learning.models import Subject
from . models import Student, CustomUser


class CustomUserCreationForm(UserCreationForm):
    """docstring for CustomUserCreationForm."""

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('username','email')#'__all__'
        # fields = UserCreationForm.Meta.fields + ('username','email')

class CustomUserChangeForm(UserChangeForm):
    """docstring for CustomUserChangeForm."""

    class Meta(UserChangeForm):
        model = CustomUser
        fields = UserChangeForm.Meta.fields #+ 'is_teacher','is_student')

class StudentSignUpForm(UserCreationForm):
    interests = forms.ModelMultipleChoiceField(
        queryset=Subject.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta(UserCreationForm.Meta):
        model = CustomUser

    @transaction.atomic# ensures that the three operations are done in a single database operation and avoids data inconsistencies in case of error
    def save(self):
        user = super().save(commit=False)
        user.is_student = True
        user.save()
        student = Student.objects.create(user=user)
        student.interests.add(*self.cleaned_data.get('interests'))
        student.save()
        return user

class TeacherSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_teacher = True
        if commit:
            user.save()
        return user
