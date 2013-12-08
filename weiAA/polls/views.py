# Create your views here.
from django.http import HttpResponse,HttpResponseRedirect
from django.template import Context,loader
from polls.models import Poll,Choice
from django.shortcuts import get_object_or_404,render
from django.core.urlresolvers import reverse
def index(request):
	
	latest_poll_list = Poll.objects.order_by('pub_date')[:5]
	#output = ', '.join(p.question for p in latest_poll_list)
	template = loader.get_template('polls/index.html')
	context = Context({
		'latest_poll_list': latest_poll_list,
	})
	return HttpResponse(template.render(context))

def details(request,poll_id):
	poll = get_object_or_404(Poll, pk=poll_id)
	return render(request,'polls/detail.html',{'poll':poll})


def vote(request,poll_id):

	p= get_object_or_404(Poll, pk=poll_id)
	try:
		selected_choice = p.choice_set.get(pk=request.POST['choice'])
	except (KeyError , Choice.DoesNotExist):
		return render(request,'polls:detail',{'poll':p,'error_message':"You didn't select a choice.", })
	else:
		selected_choice.votes += 1
		selected_choice.save()
		return HttpResponseRedirect(reverse('polls:result', args=(p.id,)))


def results(request, poll_id):
	p = get_object_or_404(Poll,pk = poll_id)
	return render(request,'polls/result.html',{'poll':p })
