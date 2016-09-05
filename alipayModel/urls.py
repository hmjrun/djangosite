from django.conf.urls import url

from . import views
app_name = 'alipayModel'
urlpatterns = [
	url(r'^$',views.index,name='index'),
	#url(r'^(?P<question_id>[0-9]+)/vote/$',views.vote,name='vote'),
	url(r'^(?P<goods_id>[0-9]+)/buy/$',views.buy,name="buy")
]