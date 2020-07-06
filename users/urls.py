from django.urls import path, include
from . views import SignupView,StudentSignUpView,TeacherSignUpView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('signup/student/', StudentSignUpView.as_view(), name='student_signup'),
    path('signup/teacher/', TeacherSignUpView.as_view(), name='teacher_signup'),
]
