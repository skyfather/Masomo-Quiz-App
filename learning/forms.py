from django import forms
from ckeditor.widgets import CKEditorWidget

from django.forms import ModelForm
from . models import Quiz, Question, Answer

class QuizForm(ModelForm):
    """docstring for QuizForm."""

    class Meta:
        model = Quiz
        # fields = ['name',]
        fields = '__all__'

class QuestionForm(ModelForm):
    """docstring for QuestionForm."""
    question = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Question
        fields = '__all__'

class AnswerForm(ModelForm):
    """docstring for AnswerForm."""
    answer = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Answer
        fields = '__all__'

class AddAnswerForm(ModelForm):
    """docstring for AddAnswerForm."""
    answer = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Answer
        fields = ['answer','is_correct']
