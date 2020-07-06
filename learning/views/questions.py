from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView#,DetailView
from django.views.generic.detail import DetailView

from .. models import Question
from .. forms import QuestionForm
from .. decorators import teacher_required


class QuestionList(ListView):
    model = Question
    paginate_by = 3
    template_name = 'learning\\question_list.html'

@method_decorator([login_required, teacher_required], name='dispatch')
class CreateQuestionView(CreateView):
    form_class = QuestionForm
    # success_url = reverse_lazy('quiz_detail')
    template_name = 'learning\\question_add.html'

class QuestionDetailView(DetailView):
    """docstring for QuizDetailView."""

    model = Question
    template_name = 'learning\\question_detail.html'
    # def get_context_data(self, **kwargs):
    #     # Call the base implementation first to get a context
    #     context = super().get_context_data(**kwargs)
    #     # Add in a QuerySet of all the questions
    #     context['answer_list'] = Answer.objects.filter(question=self.kwargs['pk'])
    #     return context

@method_decorator([login_required, teacher_required], name='dispatch')
class QuestionUpdateView(UpdateView):
    model = Question
    template_name = 'learning\\question_add.html'
    fields = '__all__'

@method_decorator([login_required, teacher_required], name='dispatch')
class QuestionDeleteView(DeleteView):
    model = Question
    success_url = reverse_lazy('question_list')
