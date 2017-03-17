import datetime
from django.db import models
from django.utils import timezone

# Create your models here.
class Question(models.Model):
	question_text = models.CharField(max_length=200)
	pub_data = models.DateTimeField('data published')

	def __str__(self):
		return self.question_text

	def was_published_recently(self):
		now = timezone.now()
		return  now - datetime.timedelta(days=1) <= self.pub_data <= now

	was_published_recently.admin_order_field = 'pub_date'
	was_published_recently.boolean = True
	was_published_recently.short_description = 'Published recently?'
    
    


class Chioce(models.Model):
	question = models.ForeignKey(Question,on_delete=models.CASCADE)
	choice_text = models.CharField(max_length=200)
	votes = models.IntegerField(default=0)

	def __str__(self):
		return self.choice_text

class Order(models.Model):
	weekday = models.IntegerField(default=0)
	point_x = models.CharField(max_length=20)
	point_y = models.CharField(max_length=20)
	order_date = models.DateTimeField()
