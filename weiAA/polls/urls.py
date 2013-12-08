from django.conf.urls import patterns , url
from polls import views
from django.views.generic import DetailView,ListView
from polls.models import Poll
urlpatterns = patterns('',
	# url(r'^$',
	# 	ListView.as_view(
	# 		queryset = Poll.objects.order_by('pub_date')[:6],
	# 		context_object_name = 'latest_poll_list',
	# 		template_name = 'polls/index.html'
	# 		),
	# 	name = 'index',
	# 	),

	# url(r'^(?P<pk>\d+)/$',
	# 	DetailView.as_view(model=Poll,
	# 		template_name = 'polls/detail.html'
	# 		),
	# 	name = 'detail'
	# 	),

	# url(r'^(?P<pk>\d+)/result/$',
	# 	DetailView.as_view(
	# 		model = Poll,
	# 		template_name='polls/result.html'
	# 	),
	# 	name = 'result'
	# 	),

	# url(r'^(?P<poll_id>\d+)/vote/$',
	# 	'polls.views.vote',name = 'vote'),
	url(r'^$',views.index, name = 'index'),
	url(r'^(?P<poll_id>\d+)/$', views.details, name='detail'),
	url(r'^(?P<poll_id>\d+)/result/$',views.results, name='result'),
	url(r'^(?P<poll_id>\d+)/vote/$', views.vote, name = 'vote'),
)
