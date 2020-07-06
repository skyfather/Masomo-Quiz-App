from django.db import models
from django.contrib.auth.models import AbstractUser

from learning.models import Quiz,Subject

# Create your models here.
class CustomUser(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)

    def get_student(self):
        return self.student

class Student(models.Model):
    """docstring for Student."""
    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE, primary_key=True)
    quizzes = models.ManyToManyField(Quiz)#, through='take_quiz')#through='QuizTakers'
    interests = models.ManyToManyField(Subject, related_name='interested_students')#related_name should be students

    def __str__(self):
        return self.user.username

    def get_interests(self):
        return self.interests.all()
        # return self.interests_set.all()

# Student.objects.get(user=s2)
# s2 = CustomUser.objects.get(id=2)
# from users.models import CustomUser
