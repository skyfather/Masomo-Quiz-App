from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView,CreateView
from django.urls import reverse_lazy

from .. models import Answer
from .. forms import AnswerForm
from .. decorators import teacher_required


class AnswerList(ListView):
    model = Answer
    template_name = 'learning\\answer_list.html'

@method_decorator([login_required, teacher_required], name='dispatch')
class CreateAnswerView(CreateView):
    form_class = AnswerForm
    # success_url = reverse_lazy('quiz_detail')
    template_name = 'learning\\create_answer.html'
    success_url = reverse_lazy('quiz_list')
    # def get(self, request, *args,**kwargs):
    #     print("----------------------------------------")
    #     print(request)
    #     print("----------------------------------------")
