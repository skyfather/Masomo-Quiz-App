from django.urls import reverse
from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
# from django.db.models.signals import pre_save
# from django.dispatch import receiver

from ckeditor.fields import RichTextField


class Subject(models.Model):
    """docstring for Subject."""

    name = models.CharField(max_length=100, unique=True)
    created_on = models.DateField(auto_now_add=True)
    updated_on = models.DateField(auto_now=True)

    def __str__(self):
        return self.name

class Quiz(models.Model):
    """docstring for Quiz."""

    name = models.CharField(max_length=100, unique=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, default=2)
    created_on = models.DateField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE)#, default=get_user_model().objects.create_user("dummyTeacher"))
    # owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)#, default=get_user_model().objects.create_user("dummyTeacher"))
    roll_out = models.BooleanField(default=False)
    # owner = models.ForeignKey('users.Teacher', on_delete=models.CASCADE)
    # questions_count = models.IntegerField(default=0)

    def get_questions(self):
        return self.question_set.all()#.select_subclasses()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('quiz_detail', kwargs={'pk': self.pk})
    class Meta:
        verbose_name = "Quiz"
        verbose_name_plural = "Quizzes"

class Question(models.Model):
    """docstring for Question."""

    # question = models.CharField(max_length=250)
    question = RichTextField()
    quiz = models.ForeignKey(Quiz,on_delete=models.CASCADE)
    updated_on = models.DateTimeField(auto_now=True)

    def get_answers(self):
        return self.answer_set.all()

    def __str__(self):
        return self.question

    def get_absolute_url(self):
        return reverse('question_detail', kwargs={'pk': self.pk})
    class Meta:
        ordering = ["updated_on"]

class Answer(models.Model):
    """docstring for Answer."""

    answer = RichTextField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.answer


class QuizTaker(models.Model):
    """docstring for QuizTakers."""

    quiz = models.ForeignKey(Quiz, related_name="quiz_taken", on_delete=models.CASCADE)
    student = models.ForeignKey('users.Student', related_name="student_taken", on_delete=models.CASCADE)
    # student = models.ForeignKey('users.CustomUser', related_name="student_taken", on_delete=models.CASCADE)
    correct_answers = models.IntegerField(default=0)
    completed = models.BooleanField(default=False)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(auto_now=True)
    # timestamp = models.DateTimeField(auto_now=True)

    def get_quiz_response(self):
        return self.quiztakerresponse_set.all()

    def __str__(self):
        return self.student.user.username

    #ensure the quiz is from the student's interests in order to take it
    def save(self, *args, **kwargs):
        if self.quiz.subject in self.student.get_interests():
            return super(QuizTaker,self).save(*args,**kwargs)

class QuizTakerResponse(models.Model):
    quiztaker = models.ForeignKey(QuizTaker, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer,on_delete=models.CASCADE,null=True,blank=True)

    def save(self, *args, **kwargs):
        if self.question.quiz != self.quiztaker.quiz:
            print(f'{self.quiztaker} has not taken QUIZ {self.question.quiz}')# Maybe we need to raise it and catch it some
            raise self.question.quiz.DoesNotExist(f"{self.quiztaker} has no interest in {self.question.quiz}")
        else:
            super(QuizTakerResponse, self).save(*args,**kwargs)

    def __str__(self):
        return self.question
