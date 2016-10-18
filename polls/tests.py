from django.test import TestCase

# Create your tests here.
import datetime
from django.utils import timezone
from .models import Question
1323456
remote change
class QuestionModelTests(TestCase):

	def test_was_published_recently_with_future_question(self):
		"""
        was_published_recently() should return False for 
        questions whose
        pub_date is in the future.
        """
		time = timezone.now() + datetime.timedelta(days=30)
		future_question = Question(pub_data = time)
		
		#We then check the output of was_published_recently() 
		#- which ought to be False.
		self.assertIs(future_question.was_published_recently(),False)
