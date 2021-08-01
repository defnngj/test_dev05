from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Question, Choice
from django.template import loader
from django.http import Http404
from django.urls import reverse
from django.views import generic


def new_index(request):
    return render(request, "polls/index.html")


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]


# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[0:5]
#     context = {
#         'latest_question_list': latest_question_list,
#     }
#     return render(request, "polls/index.html", context)


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

# def detail(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/detail.html', {'question': question})
#


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/results.html', {'question': question})
#


def vote(request, question_id):
    # print("function 1", request.POST.get('choice'))
    # print("function 2", request.POST['choice'])
    question = get_object_or_404(Question, pk=question_id)

    # question.question_text.all()
    # choice = Choice.objects.filter(question=question)

    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
    # return HttpResponse("You're voting on question %s." % question_id)














