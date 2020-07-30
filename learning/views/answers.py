from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView,CreateView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .. models import Answer
from .. forms import AnswerForm
from .. decorators import teacher_required


class AnswerList(ListView):
    model = Answer
    template_name = 'learning/answer_list.html'

@method_decorator([login_required, teacher_required], name='dispatch')
class CreateAnswerView(CreateView):
    form_class = AnswerForm
    # success_url = reverse_lazy('quiz_detail')
    template_name = 'learning/create_answer.html'
    success_url = reverse_lazy('question_list')
    # success_url = reverse_lazy('question_detail')
    # success_url = reverse_lazy('question_detail', args=[self.question.pk])
    # def get(self, request, *args,**kwargs):
    #     print("----------------------------------------")
    #     print(request)
    #     print("----------------------------------------")

class AnswerDetailView(DetailView):
    model = Answer
    template_name = 'learning/answer_detail.html'
    
@method_decorator([login_required, teacher_required], name='dispatch')
class AnswerUpdateView(UpdateView):
    model = Answer
    template_name = 'learning/create_answer.html'
    fields = '__all__'

@method_decorator([login_required, teacher_required], name='dispatch')
class AnswerDeleteView(DeleteView):
    model = Answer
    success_url = reverse_lazy('quiz_list')
