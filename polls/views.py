from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.db.models import F
from django.views import generic

from .models import Question, Choice

class IndexView(generic.ListView):
	template_name = 'polls/index.html'
	context_object_name = 'latest_question_list'

	def get_queryset(self):
		"""return last five published questions"""
		return Question.objects.order_by('-pub_date')[:5]



class DetailView(generic.DetailView):
	model = Question
	template_name = 'polls/detail.html'



class ResultsView(generic.DetailView):
	model = Question
	template_name = 'polls/results.html'



def vote(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	try: 
		selected_choice = question.choice_set.get(pk=request.POST['choice'])
	except (KeyError, choice.DoesNotExist):
		#re-display the question voting form 
		return render(request, 'polls/detail.html', {
			'question': question,
			'error_message': 'You didnt select a choice',
			})
	else:
		choice = question.choice_set.filter(pk=request.POST['choice'])
		choice.update(votes=F('votes') + 1)
		# Always return a HttpResponseRedirect after successfully dealing with POST data.
		# This prevents data from being posted twice if the user presses the back button.
		return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

