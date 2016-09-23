from django.db import models

from django.contrib.auth.models import User
from django.utils.text import slugify
from tastypie.utils.timezone import now

# Create your models here.
class Entry(models.Model):
	user 	 = 	models.ForeignKey(User)
	pub_date = 	models.DateTimeField(default=now)
	title 	 = 	models.CharField(max_length = 200)
	#当你看见当下网页url后面出现a-b-c-d-f类似的字符串，就是被slugify了
	slug 	 = 	models.SlugField()
	body 	 = 	models.TextField()

	def __str__(self):
		return self.title

	def save(self,*args,**kwargs):
		if not self.slug:
			self.slug = slugify(self.title)[:50]

		return super(Entry,self).save(*args,**kwargs)
