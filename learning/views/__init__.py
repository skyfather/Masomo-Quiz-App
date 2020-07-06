from django.views.generic import TemplateView

from .. models import Quiz, Question
from .. forms import QuizForm

class HomePageView(TemplateView):
    template_name = 'index.html'
