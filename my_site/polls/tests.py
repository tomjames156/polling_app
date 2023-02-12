import datetime


from django.utils import timezone
from django.test import TestCase
from polls.models import Question

# Create your tests here.

class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_date(self): 
        """Returns False if a question was published recently with a future date"""
    time = timezone.now() + datetime.timedelta(days=30)
    future_question  = Question(pub_date=time)
    assert(future_question.was_published_recently(), False)