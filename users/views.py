from django.shortcuts import render
from django.contrib.auth import login
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.forms import UserChangeForm

from .forms import StudentSignUpForm, TeacherSignUpForm
from .models import CustomUser


class SignupView(TemplateView):
    """docstring for Signup."""

    template_name='signup_form.html'

class StudentSignUpView(CreateView):
    model = CustomUser
    form_class = StudentSignUpForm
    template_name = 'student_signup.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'student'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('quiz_list')

class TeacherSignUpView(CreateView):
    model = CustomUser
    form_class = TeacherSignUpForm
    template_name = 'teacher_signup.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'teacher'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_staff = True
        user.save()
        try:
            group = Group.objects.get(name='Teachers')
        except Group.DoesNotExist:
            # group should exist, but this is just for safety's sake, it case the improbable should happen
            Group.objects.create(name='Teachers')
            #then add permissions to the group
            group = Group.objects.get(name='Teachers')
            quiz_create_permission = Permission.objects.get(name="Can add quiz")
            quiz_view_permission = Permission.objects.get(name="Can view quiz")
            quiz_update_permission = Permission.objects.get(name="Can change quiz")
            quiz_delete_permission = Permission.objects.get(name="Can delete quiz")
            group.permissions.add(quiz_create_permission,quiz_view_permission,quiz_update_permission,quiz_delete_permission)
        finally:
            user.groups.add(group)
        login(self.request, user)
        return redirect('create_quiz')

class ProfileUpdateView(UpdateView):
    model = CustomUser
    # form_class = UserChangeForm
    success_url = reverse_lazy('index')
    template_name = 'profile_update.html'
    fields = ('username','email','first_name','last_name')
