from django.shortcuts import get_object_or_404,render

# Create your views here.
from django.http import HttpResponseRedirect,HttpResponse
#from django.template import loader
#from django.urls import reverse
from django.views import generic
from .models import Chioce,Question,Order

class IndexView(generic.ListView):
	template_name = 'polls/index.html'
	context_object_name = 'latest_question_list'
	
	def get_queryset(self):
		return Question.objects.order_by('-pub_data')[:5]

		
# def index(request):
#     #return HttpResponse("Hello, world. You're at the polls index1.")
#     latest_question_list = Question.objects.order_by('-pub_data')[:5]
#     #output = ', '.join([q.question_text for q in latest_question_list])
#     #template = loader.get_template('polls/index.html')
#     context = {
#     	'latest_question_list':latest_question_list,
#     }
#     #return HttpResponse(template.render(context,request))
#     return render(request,'polls/index.html',context)


class DetailView(generic.DetailView):
	model = Question
	template_name = 'polls/detail.html'

# def detail(request,question_id):
# 	#return HttpResponse("You are looking at quetion %s." % question_id)
# 	# try:
# 	# 	question = Question.objects.get(pk=question_id)
# 	# except Question.DoesNotExist:
# 	# 	raise Http404("Question does not exits")
# 	question  = get_object_or_404(Question,pk=question_id)
# 	return render(request,'polls/detail.html',{'question':question})

class ResultsView(generic.DetailView):
	model = Question
	template_name = 'polls/results.html'
	
# def results(request,question_id):
# 	# response = "You are looking at the results of question %s."
# 	# return HttpResponse(response % question_id)
# 	question = get_object_or_404(Question,pk=question_id)
# 	return render(request,'polls/results.html',{'question':question})


def vote(request,question_id):
	#return HttpResponse("You are voting on quetion %s." % question_id)
	question = get_object_or_404(Question, pk=question_id)
	try:
		selected_choice = question.chioce_set.get(pk=request.POST['chioce'])
	except (KeyError,Chioce.DoesNotExist):
		return render(request,'polls/detail.html',{
			'question':question,
			'error_message':"you did not select a choice."
			})
	else:
		selected_choice.votes += 1
		selected_choice.save()
		#return HttpResponseRedirect(reverse('polls:results',args=(question.id,)))


def take_order(request):
	return render(request,'hy_order_dishes/index.html',)


from django.http  import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def take_order_data(request):
	orders = Order.objects.all()
	results = []
	for order in orders:
		s = {}
		s['weekday'] = order.weekday
		s['point'] = [order.point_x,order.point_y]
		results.append(s)
	return JsonResponse({'orders':results})

@csrf_exempt
def save_order(request):
	try:
		this_day_orders = request.POST.get('list_poits')
		points = this_day_orders.split(",")
		print (points)
		import datetime
		d=datetime.datetime.now()
		if len(points) > 0:
			for i in range(0,len(points)):
				if i%2==0:
					Order.objects.create(weekday=d.weekday()+1,point_x=points[i],point_y=points[i+1],order_date=d)
			return JsonResponse({'state':"ok"})
		else:
			return JsonResponse({'state':"no"})
	except Exception as e:
		print (e)
		raise e


