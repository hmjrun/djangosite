from django.contrib.auth.models import User
from tastypie.authorization import Authorization
from tastypie import fields
from tastypie.resources import ModelResource ,ALL ,ALL_WITH_RELATIONS
from test_tastypie.models import Entry
from django.conf.urls import url
from tastypie.utils import trailing_slash

class UserResource(ModelResource):
	class Meta:
		queryset = User.objects.all()
		resource_name = 'user'
		excludes = ['email','password','is_active','is_staff','is_superuser']
		authorization = Authorization()
		filtering = {
			'username':ALL,
		}

class EntryResource(ModelResource):
	user = fields.ForeignKey(UserResource,'user')
	class Meta:
		queryset = Entry.objects.all()
		resource_name = 'entry'
		authorization = Authorization()
		filtering = {
			'user' : ALL_WITH_RELATIONS,
			'pub_date' : ['exact','It','Ite','gte','gt'],
		}

	def prepend_urls(self):
		return [
			url(r"^(?P<resource_name>%s)/statistics%s$" % (
                self._meta.resource_name, trailing_slash()),
                self.wrap_view("get_s_data"),
                name="api_get_s_data"),
		]

	def get_s_data(self, request, **kwargs):
		result_list = []
		data = {
    		'a1':'123',
    		'a2':'123abc'
    	}
		result_list.append(data)
		return self.create_response(request, result_list)