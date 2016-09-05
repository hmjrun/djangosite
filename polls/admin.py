from django.contrib import admin

# Register your models here.
from .models import Question,Chioce
class ChoiceInline(admin.TabularInline):
	model = Chioce
	extra = 3
class QuestionAdmin(admin.ModelAdmin):
	#fields = ['pub_data','question_text']
	fieldsets = [
		(None,		{'fields':['question_text']}),
		('Date information',{'fields':['pub_data'],'classes':['collapse']}),
	]
	inlines = [ChoiceInline]

	list_display = ('question_text', 'pub_data', 'was_published_recently')

	list_filter = ['pub_data']

admin.site.register(Question,QuestionAdmin)
