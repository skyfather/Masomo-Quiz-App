from django.contrib import admin

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm

from .forms import StudentSignUpForm, TeacherSignUpForm, CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, Student

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm

# class StudentAdmin(admin.ModelAdmin):
# class StudentAdmin(UserAdmin):
#     model = CustomUser
    # add_form = StudentSignUpForm
    # form = CustomUserChangeForm
    # fields = ['pub_date', 'question_text']
admin.site.register(CustomUser, CustomUserAdmin)
# admin.site.register(CustomUser, StudentAdmin)
