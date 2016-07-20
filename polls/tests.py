import datetime

from django.utils import timezone
from django.test import TestCase
from django.core.urlresolvers import reverse

from .models import Question

def create_question(question, time):
	"""creates a question equal to question and pub_date equal to time offset from now"""

	time = timezone.now() + datetime.timedelta(hours = time)
	return Question.objects.create(question_text = question, pub_date = time)



class QuestionMethodTests(TestCase):

	def test_was_published_recently_with_future_question(self):
		"""was_published_recently() should return False for questions whose pub_date is in the future"""

		time = timezone.now() + datetime.timedelta(days=30)
		future_question = Question(pub_date=time)
		self.assertEqual(future_question.was_published_recently(), False)

	def test_was_published_recently_with_recent_question(self):
		"""was_published_recently()  should return True for questions whose pub_date is within the last day"""

		time = timezone.now() - datetime.timedelta(hours=3)
		recent_question = Question(pub_date=time)
		self.assertEqual(recent_question.was_published_recently(), True)

	def test_was_published_more_than_a_day_ago(self):
		"""was_published_recently() shoyld return False for questions whose pub_date is older than a day"""

		time = timezone.now() - datetime.timedelta(days = 2)
		old_question = Question(pub_date = time)
		self.assertEqual(old_question.was_published_recently(), False)


class QuestionViewTests(TestCase):

	def test_index_with_no_questions(self):
		"""If not questions exist a message should be displayed on the index page"""

		response = self.client.get(reverse('polls:index'))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'No polls are available')
		self.assertQuerysetEqual(response.context['latest_question_list'], [])

	def test_index_view_with_a_past_question(self):
		"""Questions with a pub_date in the past should be displayed on the index page"""

		create_question("Past question", -1)
		response = self.client.get(reverse('polls:index'))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "Past question")
		self.assertQuerysetEqual(response.context['latest_question_list'], ['<Question: Past question>'])